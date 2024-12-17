import os
from pathlib import Path
from time import sleep
import gc

import pandas as pd
import numpy as np
from dask.distributed import get_worker

from win32com.client import DispatchEx, Dispatch
from win32com.client.dynamic import CDispatch
from femtetutils import util

# noinspection PyUnresolvedReferences
from pythoncom import CoInitialize, CoUninitialize
# noinspection PyUnresolvedReferences
from pywintypes import com_error

from pyfemtet.opt import FEMInterface
from pyfemtet.core import SolveError
from pyfemtet.opt.optimizer.parameter import Parameter

from pyfemtet.dispatch_extensions import _get_pid, dispatch_specific_femtet

from pyfemtet._femtet_config_util.exit import _exit_or_force_terminate

from pyfemtet._util.excel_macro_util import watch_excel_macro_error
from pyfemtet._util.dask_util import lock_or_no_lock

from pyfemtet._warning import show_experimental_warning

from pyfemtet.opt.interface._base import logger


class ExcelInterface(FEMInterface):
    """Excel を計算コアとして利用するためのクラス。

    通常の有限要素法を Excel に
    置き換えて使用することが可能です。

    すでに Excel マクロと Femtet を
    連携させた自動解析システムを
    構築している場合、このクラスは
    それをラップします。これにより、
    PyFemtet を用いた最適化を
    行う際に便利な機能を提供します。

    Args:
        input_xlsm_path (str or Path):
            設計変数の定義を含む Excel ファイルのパスを指定
            します。
            
        input_sheet_name (str):
            設計変数の定義を含むシートの名前を指定します。
            
        output_xlsm_path (str or Path, optional):
            目的関数の定義を含む Excel ファイルのパスを指定
            します。指定しない場合は ``input_xlsm_path`` と
            同じと見做します。
            
        output_sheet_name (str, optional):
            目的関数の定義を含む含むシートの名前を指定します。
            指定しない場合は ``input_sheet_name`` と同じと見
            做します。
            
        procedure_name (str, optional):
            Excel マクロ関数名を指定します。指定しない場合は
            ``FemtetMacro.FemtetMain`` と見做します。
            
        procedure_args (list or tuple, optional):
            Excel マクロ関数に渡す引数をリストまたはタプルで
            指定します。
            
        connect_method (str, optional):
            Excel との接続方法を指定します。 'auto' または
            'new' が利用可能です。デフォルトは 'auto' です。
            
        procedure_timeout (float or None, optional):
            Excel マクロ関数のタイムアウト時間を秒単位で指定
            します。 None の場合はタイムアウトなしとなります。
            
        setup_xlsm_path (str or Path, optional):
            セットアップ時に呼ぶ関数を含む xlsm のパスです。
            指定しない場合は ``input_xlsm_path`` と
            同じと見做します。

        setup_procedure_name (str, optional):
            セットアップ時に呼ぶマクロ関数名です。
            指定しない場合、セットアップ時に何もしません。

        setup_procedure_args (list or tuple, optional):
            セットアップ時に呼ぶマクロ関数の引数です。

        teardown_xlsm_path (str or Path, optional):
            終了時に呼ぶ関数を含む xlsm のパスです。
            指定しない場合は ``input_xlsm_path`` と
            同じと見做します。

        teardown_procedure_name (str, optional):
            終了時に呼ぶマクロ関数名です。
            指定しない場合、終了時に何もしません。

        teardown_procedure_args (list or tuple, optional):
            終了時に呼ぶマクロ関数の引数です。

        visible (bool):
            excel を可視化するかどうかです。
            ただし、 True を指定した場合でもマクロの実行中は
            不可視になります。
            デフォルトは False です。

        display_alerts (bool):
            excel ダイアログを表示するかどうかです。
            デバッグ目的の場合以外は True にしないでください。
            デフォルトは False です。

        terminate_excel_when_quit (bool):
            終了時に Excel を終了するかどうかです。
            指定しない場合、 connect_method が 'new' の場合
            True とふるまい 'auto' の場合 False と振舞います。

        interactive (bool):
            excel を対話モードにするかどうかです。
            False にすると、 visible == True であっても
            自動化プロセス中にユーザーが誤って
            Excel 本体を操作できないようにします。
            デフォルトは True です。

    Attributes:
        input_xlsm_path (Path):
            設計変数の定義を含む Excel ファイルのパス。
            
        input_sheet_name (str):
            設計変数の定義を含むシートの名前。

        output_xlsm_path (Path):
            目的関数の定義を含む Excel ファイルのパス。

        output_sheet_name (str):
            目的関数の定義を含む含むシートの名前。

        procedure_name (str):
            実行する Excel マクロ関数名。

        procedure_args (list or tuple):
            Excel マクロ関数に渡す引数のリストまたはタプル。

        connect_method (str):
            接続方法。'new' または 'auto'。

        procedure_timeout (float or None):
            Excel マクロ関数の実行タイムアウト。
            Noneの場合は無制限。

        terminate_excel_when_quit (bool):
            プログラム終了時に Excel を終了するかどうか。
            connect_method が 'new' の場合 True,
            'auto' の場合 False。

        excel (CDispatch):
            Excel の COM オブジェクト。

        input_sheet (CDispatch):
            設計変数を含むシートの COM オブジェクト。

        output_sheet (CDispatch):
            目的関数を含むシートの COM オブジェクト。

        input_workbook (CDispatch):
            設計変数を含む xlsm ファイルの COM オブジェクト。

        output_workbook (CDispatch):
            設計変数を含む xlsm ファイルの COM オブジェクト。

    """

    input_xlsm_path: str  # 操作対象の xlsm パス
    input_sheet_name: str  # 変数セルを定義しているシート名
    output_xlsm_path: str  # 操作対象の xlsm パス (指定しない場合、input と同一)
    output_sheet_name: str  # 計算結果セルを定義しているシート名 (指定しない場合、input と同一)

    related_file_paths: list[str]  # 並列時に個別に並列プロセスの space にアップロードする必要のあるパス

    procedure_name: str  # マクロ関数名（or モジュール名.関数名）
    procedure_args: list  # マクロ関数の引数

    excel: CDispatch  # Excel Application
    wb_input: CDispatch  # システムを構成する Workbook
    sh_input: CDispatch  # 変数の定義された WorkSheet
    wb_output: CDispatch  # システムを構成する Workbook
    sh_output: CDispatch  # 計算結果の定義された WorkSheet (sh_input と同じでもよい)
    wb_setup: CDispatch  # システムを構成する Workbook
    wb_teardown: CDispatch  # システムを構成する Workbook

    visible: bool  # excel を可視化するかどうか
    display_alerts: bool  # ダイアログを表示するかどうか
    terminate_excel_when_quit: bool  # 終了時に Excel を終了するかどうか
    interactive: bool  # excel を対話モードにするかどうか

    _load_problem_from_me: bool = True
    _excel_pid: int
    _excel_hwnd: int
    _with_femtet_autosave_setting: bool = True  # Femtet の自動保存機能の自動設定を行うかどうか。Femtet がインストールされていない場合はオフにする。クラス変数なので、インスタンス化前に設定する。
    _femtet_autosave_buffer: bool  # Femtet の自動保存機能の一時退避場所。最適化中はオフにする。

    setup_xlsm_path: str
    setup_procedure_name: str
    setup_procedure_args: list or tuple
    teardown_xlsm_path: str
    teardown_procedure_name: str
    teardown_procedure_args: list or tuple

    def __init__(
            self,
            input_xlsm_path: str or Path,
            input_sheet_name: str,
            output_xlsm_path: str or Path = None,
            output_sheet_name: str = None,
            procedure_name: str = None,
            procedure_args: list or tuple = None,
            connect_method: str = 'auto',  # or 'new'
            procedure_timeout: float or None = None,
            setup_xlsm_path: str or Path = None,
            setup_procedure_name: str = None,
            setup_procedure_args: list or tuple = None,
            teardown_xlsm_path: str or Path = None,
            teardown_procedure_name: str = None,
            teardown_procedure_args: list or tuple = None,
            related_file_paths: list[str or Path] = None,
            visible: bool = False,
            display_alerts: bool = False,
            terminate_excel_when_quit: bool = None,
            interactive: bool = True,
    ):

        show_experimental_warning("ExcelInterface")

        # 初期化
        self.input_xlsm_path = str(input_xlsm_path)  # あとで再取得する
        self.input_sheet_name = input_sheet_name
        self.output_xlsm_path = str(input_xlsm_path) if output_xlsm_path is None else str(output_xlsm_path)
        self.output_sheet_name = output_sheet_name or self.input_sheet_name
        self.procedure_name = procedure_name or 'FemtetMacro.FemtetMain'
        self.procedure_args = procedure_args or []
        assert connect_method in ['new', 'auto']
        self.connect_method = connect_method
        self.procedure_timeout = procedure_timeout
        if terminate_excel_when_quit is None:
            self.terminate_excel_when_quit = self.connect_method == 'new'
        else:
            self.terminate_excel_when_quit = terminate_excel_when_quit

        self.setup_xlsm_path = str(input_xlsm_path) if setup_xlsm_path is None else str(setup_xlsm_path)  # あとで取得する
        self.setup_procedure_name = setup_procedure_name
        self.setup_procedure_args = setup_procedure_args or []

        self.teardown_xlsm_path = str(input_xlsm_path) if teardown_xlsm_path is None else str(teardown_xlsm_path)  # あとで取得する
        self.teardown_procedure_name = teardown_procedure_name
        self.teardown_procedure_args = teardown_procedure_args or []

        self.related_file_paths = [str(p) for p in related_file_paths] if related_file_paths is not None else []

        self.visible = visible
        self.interactive = interactive
        self.display_alerts = display_alerts

        # dask サブプロセスのときは space 直下の input_xlsm_path を参照する
        try:
            worker = get_worker()
            space = os.path.abspath(worker.local_directory)
            self.input_xlsm_path = os.path.join(space, os.path.basename(self.input_xlsm_path))
            self.output_xlsm_path = os.path.join(space, os.path.basename(self.output_xlsm_path))
            self.setup_xlsm_path = os.path.join(space, os.path.basename(self.setup_xlsm_path))
            self.teardown_xlsm_path = os.path.join(space, os.path.basename(self.teardown_xlsm_path))
            self.related_file_paths = [os.path.join(space, os.path.basename(p)) for p in self.related_file_paths]

        # main プロセスの場合は絶対パスを参照する
        except ValueError:
            self.input_xlsm_path = os.path.abspath(self.input_xlsm_path)
            self.output_xlsm_path = os.path.abspath(self.output_xlsm_path)
            self.setup_xlsm_path = os.path.abspath(self.setup_xlsm_path)
            self.teardown_xlsm_path = os.path.abspath(self.teardown_xlsm_path)
            self.related_file_paths = [os.path.abspath(p) for p in self.related_file_paths]

        # サブプロセスでの restore のための情報保管
        kwargs = dict(
            input_xlsm_path=self.input_xlsm_path,
            input_sheet_name=self.input_sheet_name,
            output_xlsm_path=self.output_xlsm_path,
            output_sheet_name=self.output_sheet_name,
            procedure_name=self.procedure_name,
            procedure_args=self.procedure_args,
            connect_method='new',  # subprocess で connect する際は new を強制する
            terminate_excel_when_quit=True,  # なので終了時は破棄する
            procedure_timeout=self.procedure_timeout,
            setup_xlsm_path=self.setup_xlsm_path,
            setup_procedure_name=self.setup_procedure_name,
            setup_procedure_args=self.setup_procedure_args,
            teardown_xlsm_path=self.teardown_xlsm_path,
            teardown_procedure_name=self.teardown_procedure_name,
            teardown_procedure_args=self.teardown_procedure_args,
            related_file_paths=self.related_file_paths,
            visible=self.visible,
            interactive=self.interactive,
            display_alerts=self.display_alerts,
        )
        FEMInterface.__init__(self, **kwargs)

    def __del__(self):
        pass

    def _setup_before_parallel(self, client) -> None:
        # メインプロセスで、並列プロセスを開始する前に行う前処理

        client.upload_file(self.input_xlsm_path, False)

        if not is_same_path(self.input_xlsm_path, self.output_xlsm_path):
            client.upload_file(self.output_xlsm_path, False)

        if not is_same_path(self.input_xlsm_path, self.setup_xlsm_path):
            client.upload_file(self.setup_xlsm_path, False)

        if not is_same_path(self.input_xlsm_path, self.teardown_xlsm_path):
            client.upload_file(self.setup_xlsm_path, False)

        for path in self.related_file_paths:
            client.upload_file(path, False)

    def _setup_after_parallel(self, *args, **kwargs):
        """サブプロセス又はメインプロセスのサブスレッドで、最適化を開始する前の前処理"""

        # kwargs で space_dir が与えられている場合、そちらを使用する
        # メインプロセスで呼ばれることを想定
        if 'space_dir' in kwargs.keys():
            space = kwargs['space_dir']
            if space is not None:
                self.input_xlsm_path = os.path.join(space, os.path.basename(self.input_xlsm_path))
                self.output_xlsm_path = os.path.join(space, os.path.basename(self.output_xlsm_path))
                self.setup_xlsm_path = os.path.join(space, os.path.basename(self.setup_xlsm_path))
                self.teardown_xlsm_path = os.path.join(space, os.path.basename(self.teardown_xlsm_path))
                self.related_file_paths = [os.path.join(space, os.path.basename(p)) for p in self.related_file_paths]

        # connect_method が auto でかつ使用中のファイルを開こうとする場合に備えて excel のファイル名を変更
        subprocess_idx = kwargs['opt'].subprocess_idx

        def proc_path(path, ignore_no_exists):
            exclude_ext, ext = os.path.splitext(path)
            new_path = exclude_ext + f'{subprocess_idx}' + ext
            if os.path.exists(path):  # input と output が同じの場合など。input がないのはおかしい
                os.rename(path, new_path)
            elif not ignore_no_exists:
                raise FileNotFoundError(f'{path} が見つかりません。')
            return new_path

        self.input_xlsm_path = proc_path(self.input_xlsm_path, False)
        self.output_xlsm_path = proc_path(self.output_xlsm_path, True)
        self.setup_xlsm_path = proc_path(self.setup_xlsm_path, True)
        self.teardown_xlsm_path = proc_path(self.teardown_xlsm_path, True)

        # スレッドが変わっているかもしれないので win32com の初期化
        CoInitialize()

        # 最適化中は femtet の autosave を無効にする
        if self._with_femtet_autosave_setting:
            from pyfemtet._femtet_config_util.autosave import _set_autosave_enabled, _get_autosave_enabled
            self._femtet_autosave_buffer = _get_autosave_enabled()
            _set_autosave_enabled(False)

        # excel に繋ぐ
        self.connect_excel(self.connect_method)

        # load_objective は 1 回目に呼ばれたのが main thread なので
        # subprocess に入った後でもう一度 load objective を行う
        from pyfemtet.opt.optimizer import AbstractOptimizer
        from pyfemtet.opt._femopt_core import Objective
        opt: AbstractOptimizer = kwargs['opt']
        obj: Objective
        for obj_name, obj in opt.objectives.items():
            if isinstance(obj.fun, ScapeGoatObjective):
                opt.objectives[obj_name].fun = self.objective_from_excel

        # excel の setup 関数を必要なら実行する
        if self.setup_procedure_name is not None:
            with lock_or_no_lock('excel_setup_procedure'):
                try:
                    with watch_excel_macro_error(self.excel, timeout=self.procedure_timeout, restore_book=False):
                        self.excel.Run(
                            f'{self.setup_procedure_name}',
                            *self.setup_procedure_args
                        )

                    # 再計算
                    self.excel.CalculateFull()

                except com_error as e:
                    raise RuntimeError(f'Failed to run macro {self.setup_procedure_args}. The original message is: {e}')

    def connect_excel(self, connect_method):

        # ===== 新しい excel instance を起動 =====
        # 起動
        if connect_method == 'auto':
            self.excel = Dispatch('Excel.Application')
        else:
            self.excel = DispatchEx('Excel.Application')

        # 起動した excel の pid を記憶する
        self._excel_hwnd = self.excel.hWnd
        self._excel_pid = 0
        while self._excel_pid == 0:
            sleep(0.5)
            self._excel_pid = _get_pid(self.excel.hWnd)

        # 可視性の設定
        self.excel.Visible = self.visible
        self.excel.DisplayAlerts = self.display_alerts
        self.excel.Interactive = self.interactive

        # 開く
        self.excel.Workbooks.Open(str(self.input_xlsm_path))
        for wb in self.excel.Workbooks:
            if wb.Name == os.path.basename(self.input_xlsm_path):
                self.wb_input = wb
                break
        else:
            raise RuntimeError(f'Cannot open {self.input_xlsm_path}')

        # シートを特定する
        for sh in self.wb_input.WorkSheets:
            if sh.Name == self.input_sheet_name:
                self.sh_input = sh
                break
        else:
            raise RuntimeError(f'Sheet {self.input_sheet_name} does not exist in the book {self.wb_input.Name}.')

        # 開く (output)
        if is_same_path(self.input_xlsm_path, self.output_xlsm_path):
            self.wb_output = self.wb_input
        else:
            self.excel.Workbooks.Open(str(self.output_xlsm_path))
            for wb in self.excel.Workbooks:
                if wb.Name == os.path.basename(self.output_xlsm_path):
                    self.wb_output = wb
                    break
            else:
                raise RuntimeError(f'Cannot open {self.output_xlsm_path}')

        # シートを特定する (output)
        for sh in self.wb_output.WorkSheets:
            if sh.Name == self.output_sheet_name:
                self.sh_output = sh
                break
        else:
            raise RuntimeError(f'Sheet {self.output_sheet_name} does not exist in the book {self.wb_output.Name}.')

        # 開く (setup)
        if is_same_path(self.input_xlsm_path, self.setup_xlsm_path):
            self.wb_setup = self.wb_input
        else:
            self.excel.Workbooks.Open(self.setup_xlsm_path)
            for wb in self.excel.Workbooks:
                if wb.Name == os.path.basename(self.setup_xlsm_path):
                    self.wb_setup = wb
                    break
            else:
                raise RuntimeError(f'Cannot open {self.setup_xlsm_path}')

        # 開く (teardown)
        if is_same_path(self.input_xlsm_path, self.teardown_xlsm_path):
            self.wb_teardown = self.wb_input
        else:
            self.excel.Workbooks.Open(self.teardown_xlsm_path)
            for wb in self.excel.Workbooks:
                if wb.Name == os.path.basename(self.teardown_xlsm_path):
                    self.wb_teardown = wb
                    break
            else:
                raise RuntimeError(f'Cannot open {self.teardown_xlsm_path}')

        # book に参照設定を追加する
        self.add_femtet_ref_xla(self.wb_input)
        self.add_femtet_ref_xla(self.wb_output)
        self.add_femtet_ref_xla(self.wb_setup)
        self.add_femtet_ref_xla(self.wb_teardown)

    def add_femtet_ref_xla(self, wb):

        # search
        ref_file_1 = r'C:\Program Files\Microsoft Office\root\Office16\XLSTART\FemtetRef.xla'
        if not os.path.exists(ref_file_1):
            # 32bit
            ref_file_1 = r'C:\Program Files (x86)\Microsoft Office\root\Office16\XLSTART\FemtetRef.xla'
        if not os.path.exists(ref_file_1):
            raise FileNotFoundError(f'{ref_file_1} not found. Please check the "Enable Macros" command was fired.')
        contain_1 = False
        for ref in wb.VBProject.References:
            if ref.FullPath is not None:
                if ref.FullPath.lower() == ref_file_1.lower():
                    contain_1 = True
        # add
        if not contain_1:
            wb.VBProject.References.AddFromFile(ref_file_1)

        # search
        ref_file_2 = os.path.abspath(util._get_femtetmacro_dllpath())
        contain_2 = False
        for ref in wb.VBProject.References:
            if ref.Description is not None:
                if ref.Description == 'FemtetMacro':  # FemtetMacro
                    contain_2 = True
        # add
        if not contain_2:
            wb.VBProject.References.AddFromFile(ref_file_2)

    def remove_femtet_ref_xla(self, wb):

        # search
        ref_file_1 = r'C:\Program Files\Microsoft Office\root\Office16\XLSTART\FemtetRef.xla'
        if not os.path.exists(ref_file_1):
            # 32bit
            ref_file_1 = r'C:\Program Files (x86)\Microsoft Office\root\Office16\XLSTART\FemtetRef.xla'
        if not os.path.exists(ref_file_1):
            raise FileNotFoundError(f'{ref_file_1} not found. Please check the "Enable Macros" command was fired.')
        for ref in wb.VBProject.References:
            if ref.FullPath is not None:
                if ref.FullPath == ref_file_1:  # or ``FemtetMacroを使用するための参照設定を自動で行ないます。``
                    wb.VBProject.References.Remove(ref)

        # search
        for ref in wb.VBProject.References:
            if ref.Description is not None:
                if ref.Description == 'FemtetMacro':  # FemtetMacro
                    wb.VBProject.References.Remove(ref)

    def update(self, parameters: pd.DataFrame) -> None:

        # params を作成
        params = dict()
        for _, row in parameters.iterrows():
            params[row['name']] = row['value']

        # excel シートの変数更新
        for key, value in params.items():
            self.sh_input.Range(key).value = value

        # 再計算
        self.excel.CalculateFull()

        # マクロ実行
        try:
            with watch_excel_macro_error(self.excel, timeout=self.procedure_timeout):
                self.excel.Run(
                    f'{self.procedure_name}',
                    *self.procedure_args
                )

            # 再計算
            self.excel.CalculateFull()

        except com_error as e:
            raise SolveError(f'Failed to run macro {self.procedure_name}. The original message is: {e}')

    def quit(self):
        if self.terminate_excel_when_quit:

            already_terminated = not hasattr(self, 'excel')
            if already_terminated:
                return

            logger.info('Excel の終了処理を開始します。')

            # 参照設定解除の前に終了処理を必要なら実施する
            # excel の setup 関数を必要なら実行する
            if self.teardown_procedure_name is not None:
                with lock_or_no_lock('excel_setup_procedure'):
                    try:
                        with watch_excel_macro_error(self.excel, timeout=self.procedure_timeout, restore_book=False):
                            self.excel.Run(
                                f'{self.teardown_procedure_name}',
                                *self.teardown_procedure_args
                            )

                        # 再計算
                        self.excel.CalculateFull()

                    except com_error as e:
                        raise RuntimeError(f'Failed to run macro {self.teardown_procedure_args}. The original message is: {e}')

            # 参照設定を解除する（不要な処理かも）
            self.remove_femtet_ref_xla(self.wb_input)
            self.remove_femtet_ref_xla(self.wb_output)
            self.remove_femtet_ref_xla(self.wb_setup)
            self.remove_femtet_ref_xla(self.wb_teardown)

            # シートの COM オブジェクト変数を削除する
            del self.sh_input
            del self.sh_output

            # workbook を閉じる
            with watch_excel_macro_error(self.excel, timeout=10, restore_book=False):
                self.wb_input.Close(SaveChanges := False)

            if not is_same_path(self.input_xlsm_path, self.output_xlsm_path):
                with watch_excel_macro_error(self.excel, timeout=10, restore_book=False):
                    self.wb_output.Close(SaveChanges := False)

            if not is_same_path(self.input_xlsm_path, self.setup_xlsm_path):
                with watch_excel_macro_error(self.excel, timeout=10, restore_book=False):
                    self.wb_setup.Close(SaveChanges := False)

            if not is_same_path(self.input_xlsm_path, self.teardown_xlsm_path):
                with watch_excel_macro_error(self.excel, timeout=10, restore_book=False):
                    self.wb_teardown.Close(SaveChanges := False)

            del self.wb_input
            del self.wb_output
            del self.wb_setup
            del self.wb_teardown


            # excel の終了
            with watch_excel_macro_error(self.excel, timeout=10, restore_book=False):
                self.excel.Quit()
            del self.excel

            # ここで Excel のプロセスが残らず落ちる
            gc.collect()

            if self._with_femtet_autosave_setting:
                from pyfemtet._femtet_config_util.autosave import _set_autosave_enabled
                logger.info('自動保存機能の設定を元に戻しています。')
                _set_autosave_enabled(self._femtet_autosave_buffer)
                logger.info('自動保存機能の設定を元に戻しました。')

    # 直接アクセスしてもよいが、ユーザーに易しい名前にするためだけのプロパティ
    @property
    def output_sheet(self) -> CDispatch:
        return self.sh_output

    @property
    def input_sheet(self) -> CDispatch:
        return self.sh_input

    @property
    def output_workbook(self) -> CDispatch:
        return self.wb_output

    @property
    def input_workbook(self) -> CDispatch:
        return self.wb_input

    def load_parameter(self, opt) -> None:
        from pyfemtet.opt.optimizer import AbstractOptimizer, logger
        opt: AbstractOptimizer

        df = pd.read_excel(
            self.input_xlsm_path,
            self.input_sheet_name,
            header=0,
            index_col=None,
        )

        # TODO: 使い勝手を考える
        for i, row in df.iterrows():
            try:
                name = row['name']
                value = row['current']
                lb = row['lower']
                ub = row['upper']
                step = row['step']
            except KeyError:
                logger.warn('列名が「name」「current」「lower」「upper」「step」になっていません。この順に並んでいると仮定して処理を続けます。')
                name, value, lb, ub, step, *_residuals = row.iloc[0]

            name = str(name)
            value = float(value)
            lb = float(lb) if not np.isnan(lb) else None
            ub = float(ub) if not np.isnan(ub) else None
            step = float(step) if not np.isnan(step) else None

            prm = Parameter(
                name=name,
                value=value,
                lower_bound=lb,
                upper_bound=ub,
                step=step,
                pass_to_fem=True,
                properties=None,
            )
            opt.variables.add_parameter(prm)

    def load_objective(self, opt):
        from pyfemtet.opt.optimizer import AbstractOptimizer, logger
        from pyfemtet.opt._femopt_core import Objective
        opt: AbstractOptimizer

        df = pd.read_excel(
            self.output_xlsm_path,
            self.output_sheet_name,
            header=0,
            index_col=None,
        )

        # TODO: 使い勝手を考える
        for i, row in df.iterrows():
            try:
                name = row['name']
                _ = row['current']
                direction = row['direction']
                value_column_index = list(df.columns).index('current')
            except KeyError:
                logger.warn('列名が「name」「current」「direction」になっていません。この順に並んでいると仮定して処理を続けます。')
                name, _, direction, *_residuals = row.iloc[0]
                value_column_index = 1

            name = str(name)

            # direction は minimize or maximize or float
            try:
                # float or not
                direction = float(direction)

            except ValueError:
                # 'minimize' or 'maximize
                direction = str(direction).lower()
                assert (direction == 'minimize') or (direction == 'maximize')

            # objective を作る
            opt.objectives[name] = Objective(
                fun=ScapeGoatObjective(),
                name=name,
                direction=direction,
                args=(i, value_column_index, ),
                kwargs=dict(),
            )

    def objective_from_excel(self, i: int, value_column_index: int):
        r = i + 2  # header が 1
        c = value_column_index + 1
        v = self.sh_output.Cells(r, c).value
        return float(v)


def wait_femtet():
    Femtet = Dispatch('FemtetMacro.Femtet')
    while Femtet.hWnd <= 0:
        sleep(1)
        Femtet = Dispatch('FemtetMacro.Femtet')


def _terminate_femtet(femtet_pid_):
    CoInitialize()
    Femtet, caught_pid = dispatch_specific_femtet(femtet_pid_)
    _exit_or_force_terminate(timeout=3, Femtet=Femtet, force=True)


# main thread で作成した excel への参照を含む関数を
# 直接 thread や process に渡すと機能しない
class ScapeGoatObjective:
    def __call__(self, *args, fem: ExcelInterface or None = None, **kwargs):
        fem.objective_from_excel(*args, **kwargs)

    @property
    def __globals__(self):
        return tuple()


def is_same_path(p1, p2):
    _p1 = os.path.abspath(p1).lower()
    _p2 = os.path.abspath(p2).lower()
    return _p1 == _p2



if __name__ == '__main__':
    ExcelInterface(..., ...)
