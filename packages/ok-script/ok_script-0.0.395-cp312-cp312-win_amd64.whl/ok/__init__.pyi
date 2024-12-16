import ctypes
import json
import os
import platform
import re
import sys
import threading
import time
from enum import IntEnum
import cv2
import numpy as np
import psutil
import win32api
import win32con
import win32gui
import win32process
import win32ui
from qfluentwidgets import FluentIcon
from ok.util.Util import is_close_to_pure_color
from ok.config.Config import Config
from ok.config.ConfigOption import ConfigOption
from ok.gui.Communicate import communicate
from ok.util.Util import get_logger
from ok.util.Util import Handler

class CaptureException(Exception):

  ...

class BaseCaptureMethod:

  def get_frame(self) -> object:
    ...

class BaseWindowsCaptureMethod(BaseCaptureMethod):

  ...

def get_crop_point(frame_width, frame_height, target_width, target_height):
  ...

class WindowsGraphicsCaptureMethod(BaseWindowsCaptureMethod):

  ...

def hwnd_window(self):
  ...

def hwnd_window(self, hwnd_window):
  ...

def connected(self):
  ...

def start_or_stop(self, capture_cursor=False):
  ...

def create_device(self):
  ...

def close(self):
  ...

def do_get_frame(self) -> object:
  ...

def reset_framepool(self, size, reset_device=False):
  ...

def crop_image(self, frame):
  ...

def crop_image(image, border, title_height):
  ...

def windows_graphics_available():
  ...

def is_blank(image):
  """
    BitBlt can return a balnk buffer. Either because the target is unsupported,
    or because there's two windows of the same name for the same executable.
    """
  ...

class BitBltCaptureMethod(BaseWindowsCaptureMethod):

  def do_get_frame(self) -> object:
    ...

def bit_blt_capture_frame(hwnd: object,
  border: int,
  title_height: int,
  width: int,
  height: int,
  _render_full_content: bool = False) -> object:
  ...

class HwndWindow:

  ...

def handle_mute(self):
  ...

def frame_ratio(self, size):
  ...

def hwnd_title(self):
  ...

def __str__(self) -> str:
  ...

def check_pos(x, y, width, height, monitors_bounds):
  ...

def get_monitors_bounds():
  ...

def is_window_in_screen_bounds(window_left, window_top, window_width, window_height, monitors_bounds):
  ...

def find_hwnd(title, exe_name, frame_width, frame_height, player_id=-1, class_name=None):
  ...

def get_mute_state(hwnd):
  ...

def set_mute_state(hwnd, mute):
  ...

def get_player_id_from_cmdline(cmdline):
  ...

def enum_child_windows(biggest, frame_aspect_ratio):
  ...

def get_exe_by_hwnd(hwnd):
  ...

class DesktopDuplicationCaptureMethod(BaseWindowsCaptureMethod):

  def do_get_frame(self) -> object:
    ...

def find_display(hmonitor, displays):
  ...

class ImageShape(IntEnum):

  ...

class ColorChannel(IntEnum):

  ...

def decimal(value: float):
  ...

def is_valid_hwnd(hwnd: int):
  """Validate the hwnd points to a valid window and not the desktop or whatever window obtained with `""`."""
  ...

def try_delete_dc(dc):
  ...

class ADBCaptureMethod(BaseCaptureMethod):

  def do_get_frame(self) -> object:
    ...

  def screencap(self) -> object:
    ...

class ImageCaptureMethod(BaseCaptureMethod):

  def do_get_frame(self) -> object:
    ...

class DeviceManager:

  def __init__(self, app_config, exit_event=None, global_config=None):
    ...

from ok.interaction.PyDirectInteraction import PyDirectInteraction

def refresh(self):
  ...

def adb(self):
  ...

def try_kill_adb(self, e=None):
  ...

def adb_connect(self, addr, try_connect=True):
  ...

def get_devices(self):
  ...

def update_pc_device(self):
  ...

def do_refresh(self, current=False):
  ...

def refresh_phones(self, current=False):
  ...

def refresh_emulators(self, current=False):
  ...

def get_resolution(self, device=None):
  ...

def set_preferred_device(self, imei=None, index=-1):
  ...

def shell_device(self, device, *args, **kwargs):
  ...

def adb_get_imei(self, device):
  ...

def get_preferred_device(self):
  ...

def get_preferred_capture(self):
  ...

def set_hwnd_name(self, hwnd_name):
  ...

def set_capture(self, capture):
  ...

def get_hwnd_name(self):
  ...

def ensure_hwnd(self, title, exe, frame_width=0, frame_height=0, player_id=-1, hwnd_class=None):
  ...

def use_windows_capture(self, override_config=None, require_bg=False, use_bit_blt_only=False, bit_blt_render_full=False):
  ...

def start(self):
  ...

def do_start(self):
  ...

def update_resolution_for_hwnd(self):
  ...

def device(self):
  ...

def adb_kill_server(self):
  ...

def width(self):
  ...

def height(self):
  ...

def update_device_list(self):
  ...

def shell(self, *args, **kwargs):
  ...

def device_connected(self):
  ...

def get_exe_path(self, device):
  ...

from ok.alas.platform_windows import get_emulator_exe

def adb_check_installed(self, packages):
  ...

def adb_check_in_front(self, packages):
  ...

def adb_start_package(self, package):
  ...

def adb_ensure_in_front(self, packages):
  ...

def parse_ratio(ratio_str):
  ...

class NemuIpcCaptureMethod(BaseCaptureMethod):

  def do_get_frame(self) -> object:
    ...

  def screencap(self) -> object:
    ...

def deep_get(d, keys, default=None):
  """
    Get values in dictionary safely.
    https://stackoverflow.com/questions/25833613/safe-method-to-get-value-of-nested-dictionary

    Args:
        d (dict):
        keys (str, list): Such as `Scheduler.NextRun.value`
        default: Default return if key not found.

    Returns:

    """
  ...

def update_capture_method(config,
  capture_method,
  hwnd,
  require_bg=False,
  use_bit_blt_only=False,
  bit_blt_render_full=False,
  exit_event=None):
  ...

def get_win_graphics_capture(capture_method, hwnd, exit_event):
  ...

def get_capture(capture_method, target_method, hwnd, exit_event):
  ...

def is_window_minimized(hWnd):
  ...

def get_window_bounds(hwnd):
  ...

def is_foreground_window(hwnd):
  ...

def resize_window(hwnd, width, height):
  ...

def compare_strings_safe(str1: str, str2: str) -> bool:
  ...

from _typeshed import Incomplete
from ok.capture.adb.nemu_utils import RETRY_TRIES as RETRY_TRIES, retry_sleep as retry_sleep
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class NemuIpcIncompatible(Exception): ...
class NemuIpcError(Exception): ...

class CaptureStd:
    stdout: bytes
    stderr: bytes
    def __init__(self) -> None: ...
    fdout: Incomplete
    fderr: Incomplete
    old_stdout: Incomplete
    old_stderr: Incomplete
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None) -> None: ...
    @staticmethod
    def recvall(reader, length: int = 1024) -> bytes: ...

class CaptureNemuIpc(CaptureStd):
    instance: Incomplete
    def is_capturing(self): ...
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None) -> None: ...
    def check_stdout(self) -> None: ...
    def check_stderr(self) -> None: ...

def retry(func): ...

class NemuIpcImpl:
    nemu_folder: Incomplete
    instance_id: Incomplete
    display_id: Incomplete
    ev: Incomplete
    lib: Incomplete
    connect_id: int
    width: int
    height: int
    def __init__(self, nemu_folder: str, instance_id: int, display_id: int = 0) -> None: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def reconnect(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None) -> None: ...
    async def ev_run_async(self, func, *args, timeout: float = 0.15, **kwargs): ...
    def ev_run_sync(self, func, *args, **kwargs): ...
    def get_resolution(self) -> None: ...
    def screenshot(self, timeout: float = 0.15): ...
    def convert_xy(self, x, y): ...
    def down(self, x, y) -> None: ...
    def up(self) -> None: ...
    @staticmethod
    def serial_to_id(serial: str): ...

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete
RETRY_TRIES: int
RETRY_DELAY: int

def is_port_using(port_num): ...
def random_port(port_range): ...
def recv_all(stream, chunk_size: int = 4096, recv_interval: float = 0.0) -> bytes: ...
def possible_reasons(*args) -> None: ...

class PackageNotInstalled(Exception): ...
class ImageTruncated(Exception): ...

def retry_sleep(trial) -> None: ...
def handle_adb_error(e): ...
def handle_unknown_host_service(e): ...
def get_serial_pair(serial): ...
def remove_prefix(s, prefix): ...
def remove_suffix(s, suffix): ...
def remove_shell_warning(s): ...

import ctypes
from _typeshed import Incomplete
from ok.rotypes import IUnknown as IUnknown, idldsl as idldsl

D3D11_SDK_VERSION: int
D3D_DRIVER_TYPE_HARDWARE: int
D3D11_CREATE_DEVICE_BGRA_SUPPORT: int
D3D11_USAGE_STAGING: int
D3D11_CPU_ACCESS_READ: int
D3D11_MAP_READ: int
DXGI_ERROR_DEVICE_REMOVED: int
DXGI_ERROR_DEVICE_RESET: int

class DXGI_SAMPLE_DESC(ctypes.Structure): ...
class D3D11_TEXTURE2D_DESC(ctypes.Structure): ...
class D3D11_MAPPED_SUBRESOURCE(ctypes.Structure): ...
class ID3D11Device(IUnknown): ...
class ID3D11Texture2D(IUnknown): ...
class ID3D11DeviceContext(IUnknown): ...

D3D11CreateDevice: Incomplete

from ok.util.Util import get_relative_path as get_relative_path

def get_thread_name(thread_id): ...
def dump_threads() -> None: ...
def kill_dump() -> None: ...
def console_handler(event): ...

import numpy as np
import os
from _typeshed import Incomplete
from _win32typing import PyCDC as PyCDC
from collections.abc import Callable as Callable, Iterable
from enum import IntEnum
from itertools import chain
from typing import Any, TypeGuard, TypeVar

T = TypeVar('T')
ONE_SECOND: int
DWMWA_EXTENDED_FRAME_BOUNDS: int
MAXBYTE: int
BGR_CHANNEL_COUNT: int
BGRA_CHANNEL_COUNT: int

class ImageShape(IntEnum):
    Y = 0
    X = 1
    Channels = 2

class ColorChannel(IntEnum):
    Blue = 0
    Green = 1
    Red = 2
    Alpha = 3

def decimal(value: float): ...
def is_digit(value: str | int | None): ...
def is_valid_image(image: np.ndarray | None) -> TypeGuard[np.ndarray]: ...
def is_valid_hwnd(hwnd: int): ...
def first(iterable: Iterable[T]) -> T: ...
def try_delete_dc(dc: PyCDC): ...
def open_file(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]): ...
def get_or_create_eventloop(): ...
def fire_and_forget(func: Callable[..., Any]): ...
def flatten(nested_iterable: Iterable[Iterable[T]]) -> chain[T]: ...

WINDOWS_BUILD_NUMBER: Incomplete
FIRST_WIN_11_BUILD: int
WGC_MIN_BUILD: int
FROZEN: Incomplete
auto_split_directory: Incomplete

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

MDT_EFFECTIVE_DPI: int
user32: Incomplete
DWMWA_EXTENDED_FRAME_BOUNDS: int
logger: Incomplete

def is_window_minimized(hWnd): ...
def get_window_bounds(hwnd): ...
def is_foreground_window(hwnd): ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import get_logger as get_logger, get_relative_path as get_relative_path, read_json_file as read_json_file, write_json_file as write_json_file

logger: Incomplete

class Config(dict):
    config_folder: str
    default: Incomplete
    validator: Incomplete
    config_file: Incomplete
    def __init__(self, name, default, folder: Incomplete | None = None, validator: Incomplete | None = None) -> None: ...
    def save_file(self) -> None: ...
    def reset_to_default(self) -> None: ...
    def pop(self, key, default: Incomplete | None = None): ...
    def popitem(self): ...
    def clear(self) -> None: ...
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def has_user_config(self): ...
    def validate(self, key, value): ...
    def verify_config(self, current, default_config): ...

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class ConfigOption:
    name: Incomplete
    description: Incomplete
    default_config: Incomplete
    config_description: Incomplete
    config_type: Incomplete
    validator: Incomplete
    icon: Incomplete
    def __init__(self, name, default: Incomplete | None = None, description: str = '', config_description: Incomplete | None = None, config_type: Incomplete | None = None, validator: Incomplete | None = None, icon=...) -> None: ...

from _typeshed import Incomplete
from ok.config.Config import Config as Config
from ok.config.ConfigOption import ConfigOption as ConfigOption

class GlobalConfig:
    configs: Incomplete
    config_options: Incomplete
    lock: Incomplete
    def __init__(self) -> None: ...
    def get_config(self, option: ConfigOption): ...
    def get_all_visible_configs(self): ...

class InfoDict(dict):
    def __delitem__(self, key) -> None: ...
    def clear(self) -> None: ...
    def __setitem__(self, key, value) -> None: ...

from _typeshed import Incomplete
from ok.display.windows_types import DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO as DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO, DISPLAYCONFIG_MODE_INFO as DISPLAYCONFIG_MODE_INFO

class DisplayMode:
    width: Incomplete
    height: Incomplete
    refresh: Incomplete
    def __init__(self, width: int, height: int, refresh: int) -> None: ...

class DisplayAdapter:
    identifier: Incomplete
    display_name: Incomplete
    active_mode: Incomplete
    available_modes: Incomplete
    is_attached: Incomplete
    is_primary: Incomplete
    def __init__(self, identifier: str = '', display_name: str = '', active_mode: DisplayMode | None = None, available_modes: list[DisplayMode] | None = None, is_attached: bool = False, is_primary: bool = False) -> None: ...

class DisplayMonitor:
    name: Incomplete
    adapter: Incomplete
    mode_info: Incomplete
    color_info: Incomplete
    def __init__(self, name: str = '', adapter: DisplayAdapter = ..., mode_info: DISPLAYCONFIG_MODE_INFO | None = None, color_info: DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO | None = None) -> None: ...
    def identifier(self) -> str: ...
    def active_mode(self) -> DisplayMode | None: ...
    def is_primary(self) -> bool: ...
    def is_attached(self) -> bool: ...
    def is_hdr_supported(self) -> bool: ...
    def is_hdr_enabled(self) -> bool: ...

class DisplayMonitorException(Exception): ...
class PrimaryMonitorException(Exception): ...
class HdrException(Exception): ...
class DisplayAdapterException(Exception): ...

from _typeshed import Incomplete
from ok.display.custom_types import DisplayMonitor as DisplayMonitor
from ok.display.display_monitors import get_all_display_monitors as get_all_display_monitors
from ok.util.Util import get_logger as get_logger

logger: Incomplete

def is_night_light_enabled(): ...
def is_hdr_enabled(): ...

from ok.display.custom_types import DisplayAdapter as DisplayAdapter, DisplayAdapterException as DisplayAdapterException, DisplayMode as DisplayMode
from ok.display.windows_types import ChangeDisplaySettingsExW as ChangeDisplaySettingsExW, DEVMODEW as DEVMODEW, DISPLAY_DEVICEW as DISPLAY_DEVICEW, DISPLAY_DEVICE_ATTACHED_TO_DESKTOP as DISPLAY_DEVICE_ATTACHED_TO_DESKTOP, DISPLAY_DEVICE_PRIMARY_DEVICE as DISPLAY_DEVICE_PRIMARY_DEVICE, DISP_CHANGE_BADDUALVIEW as DISP_CHANGE_BADDUALVIEW, DISP_CHANGE_BADFLAGS as DISP_CHANGE_BADFLAGS, DISP_CHANGE_BADMODE as DISP_CHANGE_BADMODE, DISP_CHANGE_BADPARAM as DISP_CHANGE_BADPARAM, DISP_CHANGE_FAILED as DISP_CHANGE_FAILED, DISP_CHANGE_NOTUPDATED as DISP_CHANGE_NOTUPDATED, DISP_CHANGE_RESTART as DISP_CHANGE_RESTART, DISP_CHANGE_SUCCESSFUL as DISP_CHANGE_SUCCESSFUL, DM_DISPLAYFREQUENCY as DM_DISPLAYFREQUENCY, DM_PELSHEIGHT as DM_PELSHEIGHT, DM_PELSWIDTH as DM_PELSWIDTH, ENUM_CURRENT_SETTINGS as ENUM_CURRENT_SETTINGS, EnumDisplayDevicesW as EnumDisplayDevicesW, EnumDisplaySettingsW as EnumDisplaySettingsW

def is_attached_to_desktop(adapter: DISPLAY_DEVICEW) -> bool: ...
def is_primary_device(adapter: DISPLAY_DEVICEW) -> bool: ...
def get_all_display_adapters() -> list[DisplayAdapter]: ...
def get_all_available_display_modes_for_adapter(adapter: DISPLAY_DEVICEW) -> list[DisplayMode]: ...
def get_active_display_mode_for_adapter(adapter: DISPLAY_DEVICEW) -> DisplayMode: ...
def set_display_mode_for_device(display_mode: DisplayMode, device_identifier: str): ...

from ok.display.custom_types import DisplayMonitor as DisplayMonitor, DisplayMonitorException as DisplayMonitorException, PrimaryMonitorException as PrimaryMonitorException
from ok.display.display_adapters import DisplayAdapter as DisplayAdapter, get_all_display_adapters as get_all_display_adapters
from ok.display.windows_types import DISPLAYCONFIG_ADAPTER_NAME as DISPLAYCONFIG_ADAPTER_NAME, DISPLAYCONFIG_DEVICE_INFO_TYPE as DISPLAYCONFIG_DEVICE_INFO_TYPE, DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO as DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO, DISPLAYCONFIG_MODE_INFO as DISPLAYCONFIG_MODE_INFO, DISPLAYCONFIG_PATH_INFO as DISPLAYCONFIG_PATH_INFO, DISPLAYCONFIG_PATH_SOURCE_INFO as DISPLAYCONFIG_PATH_SOURCE_INFO, DISPLAYCONFIG_SET_ADVANCED_COLOR_STATE as DISPLAYCONFIG_SET_ADVANCED_COLOR_STATE, DISPLAYCONFIG_SOURCE_DEVICE_NAME as DISPLAYCONFIG_SOURCE_DEVICE_NAME, DISPLAYCONFIG_TARGET_DEVICE_NAME as DISPLAYCONFIG_TARGET_DEVICE_NAME, DisplayConfigGetDeviceInfo as DisplayConfigGetDeviceInfo, DisplayConfigSetDeviceInfo as DisplayConfigSetDeviceInfo, ERROR_SUCCESS as ERROR_SUCCESS, GetDisplayConfigBufferSizes as GetDisplayConfigBufferSizes, QDC_ONLY_ACTIVE_PATHS as QDC_ONLY_ACTIVE_PATHS, QueryDisplayConfig as QueryDisplayConfig

def get_adapter_name(mode_info: DISPLAYCONFIG_MODE_INFO) -> str: ...
def get_monitor_source_name(path_source_info: DISPLAYCONFIG_PATH_SOURCE_INFO) -> str: ...
def get_monitor_name(mode_info: DISPLAYCONFIG_MODE_INFO) -> str: ...
def get_monitor_color_info(mode_info: DISPLAYCONFIG_MODE_INFO) -> DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO: ...
def set_hdr_state_for_monitor(enabled: bool, monitor: DisplayMonitor): ...
def get_primary_monitor(monitors: list[DisplayMonitor]) -> DisplayMonitor: ...
def get_all_display_monitors() -> list[DisplayMonitor]: ...

from _typeshed import Incomplete
from ctypes import Structure, Union
from enum import IntEnum

CCHDEVICENAME: int
ERROR_SUCCESS: int
ERROR_INVALID_PARAMETER: int
ERROR_NOT_SUPPORTED: int
ERROR_ACCESS_DENIED: int
ERROR_GEN_FAILURE: int
ERROR_INSUFFICIENT_BUFFER: int
QDC_ONLY_ACTIVE_PATHS: int
DISPLAYCONFIG_PATH_ACTIVE: int
ENUM_CURRENT_SETTINGS: int
DM_PELSWIDTH: int
DM_PELSHEIGHT: int
DM_DISPLAYFLAGS: int
DM_DISPLAYFREQUENCY: int
DISPLAY_DEVICE_ATTACHED_TO_DESKTOP: int
DISPLAY_DEVICE_PRIMARY_DEVICE: int
DISP_CHANGE_SUCCESSFUL: int
DISP_CHANGE_RESTART: int
DISP_CHANGE_FAILED: int
DISP_CHANGE_BADMODE: int
DISP_CHANGE_NOTUPDATED: int
DISP_CHANGE_BADFLAGS: int
DISP_CHANGE_BADPARAM: int
DISP_CHANGE_BADDUALVIEW: int

class LUID(Structure): ...
class PATH_INFO_DUMMY_STRUCT_NAME(Structure): ...
class PATH_INFO_DUMMY_UNION_NAME(Union): ...
class DISPLAYCONFIG_PATH_SOURCE_INFO(Structure): ...

class DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY(IntEnum):
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_OTHER = 0
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15 = 1
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SVIDEO = 2
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPOSITE_VIDEO = 3
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPONENT_VIDEO = 4
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI = 5
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI = 6
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_LVDS = 7
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_D_JPN = 8
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDI = 9
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL = 10
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EMBEDDED = 11
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EXTERNAL = 12
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EMBEDDED = 13
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDTVDONGLE = 14
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_MIRACAST = 15
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_WIRED = 16
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INDIRECT_VIRTUAL = 17
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL = 2147483648
    DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32 = 4294967295

class DISPLAYCONFIG_ROTATION(IntEnum):
    DISPLAYCONFIG_ROTATION_IDENTITY = 1
    DISPLAYCONFIG_ROTATION_ROTATE90 = 2
    DISPLAYCONFIG_ROTATION_ROTATE180 = 3
    DISPLAYCONFIG_ROTATION_ROTATE270 = 4
    DISPLAYCONFIG_ROTATION_FORCE_UINT32 = 4294967295

class DISPLAYCONFIG_SCALING(IntEnum):
    DISPLAYCONFIG_SCALING_IDENTITY = 1
    DISPLAYCONFIG_SCALING_CENTERED = 2
    DISPLAYCONFIG_SCALING_STRETCHED = 3
    DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX = 4
    DISPLAYCONFIG_SCALING_CUSTOM = 5
    DISPLAYCONFIG_SCALING_PREFERRED = 128

class DISPLAYCONFIG_RATIONAL(Structure): ...

class DISPLAYCONFIG_SCANLINE_ORDERING(IntEnum):
    DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED = 0
    DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE = 1
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED = 2

class DISPLAYCONFIG_PATH_TARGET_INFO(Structure): ...

class DISPLAYCONFIG_MODE_INFO_TYPE(IntEnum):
    DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE = 1
    DISPLAYCONFIG_MODE_INFO_TYPE_TARGET = 2
    DISPLAYCONFIG_MODE_INFO_TYPE_DESKTOP_IMAGE = 3
    DISPLAYCONFIG_MODE_INFO_TYPE_FORCE_UINT32 = 4294967295

class DISPLAYCONFIG_2DREGION(Structure): ...
class DISPLAYCONFIG_DUMMY_STRUCT_NAME(Structure): ...
class DISPLAYCONFIG_DUMMY_UNION_NAME(Union): ...
class DISPLAYCONFIG_VIDEO_SIGNAL_INFO(Structure): ...
class DISPLAYCONFIG_TARGET_MODE(Structure): ...

class DISPLAYCONFIG_PIXELFORMAT(IntEnum):
    DISPLAYCONFIG_PIXELFORMAT_8BPP = 1
    DISPLAYCONFIG_PIXELFORMAT_16BPP = 2
    DISPLAYCONFIG_PIXELFORMAT_24BPP = 3
    DISPLAYCONFIG_PIXELFORMAT_32BPP = 4
    DISPLAYCONFIG_PIXELFORMAT_NONGDI = 5
    DISPLAYCONFIG_PIXELFORMAT_FORCE_UINT32 = 4294967295

class DISPLAYCONFIG_SOURCE_MODE(Structure): ...
class DISPLAYCONFIG_DESKTOP_IMAGE_INFO(Structure): ...
class DISPLAYCONFIG_MODE_INFO_DUMMY_UNION_NAME(Union): ...
class DISPLAYCONFIG_MODE_INFO(Structure): ...
class DISPLAYCONFIG_PATH_INFO(Structure): ...

class DISPLAYCONFIG_DEVICE_INFO_TYPE(IntEnum):
    DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME = 1
    DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME = 2
    DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_PREFERRED_MODE = 3
    DISPLAYCONFIG_DEVICE_INFO_GET_ADAPTER_NAME = 4
    DISPLAYCONFIG_DEVICE_INFO_SET_TARGET_PERSISTENCE = 5
    DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_BASE_TYPE = 6
    DISPLAYCONFIG_DEVICE_INFO_GET_SUPPORT_VIRTUAL_RESOLUTION = 7
    DISPLAYCONFIG_DEVICE_INFO_SET_SUPPORT_VIRTUAL_RESOLUTION = 8
    DISPLAYCONFIG_DEVICE_INFO_GET_ADVANCED_COLOR_INFO = 9
    DISPLAYCONFIG_DEVICE_INFO_SET_ADVANCED_COLOR_STATE = 10
    DISPLAYCONFIG_DEVICE_INFO_GET_SDR_WHITE_LEVEL = 11
    DISPLAYCONFIG_DEVICE_INFO_FORCE_UINT32 = 4294967295

class DISPLAYCONFIG_DEVICE_INFO_HEADER(Structure): ...

class DISPLAYCONFIG_COLOR_ENCODING(IntEnum):
    DISPLAYCONFIG_COLOR_ENCODING_RGB = 0
    DISPLAYCONFIG_COLOR_ENCODING_YCBCR444 = 1
    DISPLAYCONFIG_COLOR_ENCODING_YCBCR422 = 2
    DISPLAYCONFIG_COLOR_ENCODING_YCBCR420 = 3
    DISPLAYCONFIG_COLOR_ENCODING_INTENSITY = 4

class DISPLAYCONFIG_GET_ADVANCED_COLOR_INFO(Structure): ...
class DISPLAYCONFIG_SOURCE_DEVICE_NAME(Structure): ...
class DISPLAYCONFIG_TARGET_DEVICE_NAME_FLAGS(Structure): ...
class DISPLAYCONFIG_TARGET_DEVICE_NAME(Structure): ...
class DISPLAYCONFIG_ADAPTER_NAME(Structure): ...
class DEMOVEDW_DUMMY_STRUCT_NAME(Structure): ...
class DEVMODEW_DUMMY_STRUCT_NAME2(Structure): ...
class DEVMODEW_DUMMY_UNION_NAME(Union): ...
class DEVMODEW_DUMMY_UNION_NAME2(Union): ...
class DEVMODEW(Structure): ...
class DISPLAY_DEVICEW(Structure): ...
class DISPLAYCONFIG_SET_ADVANCED_COLOR_STATE(Structure): ...

user32DLL: Incomplete
ChangeDisplaySettingsExW: Incomplete
EnumDisplaySettingsW: Incomplete
EnumDisplayDevicesW: Incomplete
DisplayConfigGetDeviceInfo: Incomplete
DisplayConfigSetDeviceInfo: Incomplete
GetDisplayConfigBufferSizes: Incomplete
QueryDisplayConfig: Incomplete

from _typeshed import Incomplete
from ok.feature.FeatureSet import load_json as load_json, read_from_json as read_from_json
from ok.util.Util import get_logger as get_logger

logger: Incomplete

def compress_coco(coco_json) -> None: ...
def replace_extension(i, file_name): ...
def save_image_with_metadata(image, image_path, new_path): ...

import numpy as np
from _typeshed import Incomplete

class Feature:
    mat: Incomplete
    x: Incomplete
    y: Incomplete
    mask: Incomplete
    def __init__(self, mat: np.ndarray, x: int = 0, y: int = 0, scaling: int = 1) -> None: ...
    @property
    def width(self): ...
    @property
    def height(self): ...
    def scaling(self): ...

import numpy as np
from _typeshed import Incomplete
from ok.feature.Feature import Feature as Feature
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import Box as Box, get_logger as get_logger, get_path_relative_to_exe as get_path_relative_to_exe, rgb_to_gray as rgb_to_gray, sort_boxes as sort_boxes

logger: Incomplete

class FeatureSet:
    feature_dict: dict[str, Feature]
    box_dict: dict[str, Box]
    load_success: bool
    coco_json: Incomplete
    debug: Incomplete
    width: int
    height: int
    default_threshold: Incomplete
    default_horizontal_variance: Incomplete
    default_vertical_variance: Incomplete
    lock: Incomplete
    def __init__(self, debug, coco_json: str, default_horizontal_variance: int = 0, default_vertical_variance: int = 0, default_threshold: float = 0.95) -> None: ...
    def feature_exists(self, feature_name: str) -> bool: ...
    def empty(self): ...
    def check_size(self, frame): ...
    def process_data(self) -> bool: ...
    def get_box_by_name(self, mat, category_name: str) -> Box: ...
    def save_images(self, target_folder: str) -> None: ...
    def get_feature_by_name(self, name): ...
    def find_one_feature(self, mat: np.ndarray, category_name: str, horizontal_variance: float = 0, vertical_variance: float = 0, threshold: float = 0, use_gray_scale: bool = False, x: int = -1, y: int = -1, to_x: int = -1, to_y: int = -1, width: int = -1, height: int = -1, box: Incomplete | None = None, canny_lower: int = 0, canny_higher: int = 0, inverse_mask_color: Incomplete | None = None, frame_processor: Incomplete | None = None, template: Incomplete | None = None, mask_function: Incomplete | None = None) -> list[Box]: ...
    def find_feature(self, mat: np.ndarray, category_name, horizontal_variance: float = 0, vertical_variance: float = 0, threshold: float = 0, use_gray_scale: bool = False, x: int = -1, y: int = -1, to_x: int = -1, to_y: int = -1, width: int = -1, height: int = -1, box: Incomplete | None = None, canny_lower: int = 0, canny_higher: int = 0, inverse_mask_color: Incomplete | None = None, frame_processor: Incomplete | None = None, template: Incomplete | None = None, mask_function: Incomplete | None = None) -> list[Box]: ...

def read_from_json(coco_json, width: int = -1, height: int = -1): ...
def load_json(coco_json): ...
def un_fk_label_studio_path(path): ...
def adjust_coordinates(x, y, w, h, screen_width, screen_height, image_width, image_height, hcenter: bool = False): ...
def scale_by_anchor(x, image_width, screen_width, scale, hcenter: bool = False): ...
def replace_extension(filename): ...
def filter_and_sort_matches(result, threshold, w, h): ...
def mask_white(image, lower_white: int = 255): ...

import hashlib
import sys
import uuid
import requests
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
import ok
from ok.analytics.Analytics import Analytics
from ok.config.Config import Config
from ok.gui.Communicate import communicate
from ok.gui.MainWindow import MainWindow
from ok.gui.MessageWindow import MessageWindow
from ok.gui.StartController import StartController
from ok.gui.common.config import Language
from ok.gui.i18n.GettextTranslator import get_translations
from ok.gui.overlay.OverlayWindow import OverlayWindow
from ok.gui.util.app import init_app_config
from ok.util.Util import get_logger
from ok.main.globals import og
from ok.update.GitUpdater import GitUpdater
from ok.util.Util import Handler
from ok.util.Util import get_path_relative_to_exe
from ok.util.Util import init_class_by_name

class App:

  ...

def update_overlay(self, visible, x, y, window_width, window_height, width, height, scaling):
  ...

def show_main_window(self):
  ...

def do_show_main(self):
  ...

def exec(self):
  ...

def get_my_id():
  ...

class Response:

  ...

def r(path: str, params: dict):
  ...

def d(data: bytes) -> bytes:
  ...

def e(data: bytes) -> bytes:
  ...

from PySide6.QtCore import QObject, Signal
from _typeshed import Incomplete

class Communicate(QObject):
    log: Incomplete
    fps: Incomplete
    frame_time: Incomplete
    scene: Incomplete
    draw_box: Incomplete
    task: Incomplete
    task_done: Incomplete
    window: Incomplete
    loading_progress: Incomplete
    notification: Incomplete
    executor_paused: Signal
    screenshot: Incomplete
    adb_devices: Signal
    config_validation: Signal
    tab: Incomplete
    capture_error: Incomplete
    check_update: Incomplete
    download_update: Incomplete
    starting_emulator: Incomplete
    quit: Incomplete
    update_running: Incomplete
    versions: Incomplete
    launcher_profiles: Incomplete
    update_logs: Incomplete
    update_download_percent: Incomplete
    cuda_version: Incomplete
    start_success: Incomplete
    def emit_draw_box(self, key: str = None, boxes: Incomplete | None = None, color: Incomplete | None = None, frame: Incomplete | None = None): ...

communicate: Incomplete

from PySide6.QtCore import QObject as QObject
from _typeshed import Incomplete
from ok.config.Config import Config as Config
from ok.config.ConfigOption import ConfigOption as ConfigOption
from ok.gui.Communicate import communicate as communicate
from ok.gui.about.AboutTab import AboutTab as AboutTab
from ok.gui.act.ActTab import ActTab as ActTab
from ok.gui.debug.DebugTab import DebugTab as DebugTab
from ok.gui.settings.SettingTab import SettingTab as SettingTab
from ok.gui.start.StartTab import StartTab as StartTab
from ok.gui.tasks.OneTimeTaskTab import OneTimeTaskTab as OneTimeTaskTab
from ok.gui.tasks.TriggerTaskTab import TriggerTaskTab as TriggerTaskTab
from ok.gui.util.Alert import alert_error as alert_error
from ok.gui.util.app import show_info_bar as show_info_bar
from ok.gui.widget.StartLoadingDialog import StartLoadingDialog as StartLoadingDialog
from ok.main.globals import og as og
from ok.util.Util import get_logger as get_logger, init_class_by_name as init_class_by_name
from qfluentwidgets import MSFluentWindow

auto_start_config_option: Incomplete
logger: Incomplete

class MainWindow(MSFluentWindow):
    act: Incomplete
    app: Incomplete
    ok_config: Incomplete
    auto_start_config: Incomplete
    main_window_config: Incomplete
    original_layout: Incomplete
    exit_event: Incomplete
    start_tab: Incomplete
    onetime_tab: Incomplete
    trigger_tab: Incomplete
    emulator_starting_dialog: Incomplete
    do_not_quit: bool
    first_task_tab: Incomplete
    about_tab: Incomplete
    act_tab: Incomplete
    tray: Incomplete
    def __init__(self, app, config, ok_config, icon, title, version, debug: bool = False, about: Incomplete | None = None, exit_event: Incomplete | None = None) -> None: ...
    def showEvent(self, event) -> None: ...
    def set_window_size(self, width, height, min_width, min_height) -> None: ...
    def do_check_auth(self) -> None: ...
    def show_act(self) -> None: ...
    def eventFilter(self, obj, event): ...
    def update_ok_config(self) -> None: ...
    def starting_emulator(self, done, error, seconds_left) -> None: ...
    def config_validation(self, message) -> None: ...
    def show_notification(self, message, title: Incomplete | None = None, error: bool = False, tray: bool = False) -> None: ...
    def capture_error(self) -> None: ...
    def navigate_tab(self, index) -> None: ...
    def executor_paused(self, paused) -> None: ...
    def closeEvent(self, event) -> None: ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.common.style_sheet import StyleSheet as StyleSheet
from ok.gui.widget.BaseWindow import BaseWindow as BaseWindow
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class MessageWindow(BaseWindow):
    exit_event: Incomplete
    message: Incomplete
    title_bar: Incomplete
    message_label: Incomplete
    vBoxLayout: Incomplete
    confirm_button: Incomplete
    def __init__(self, icon, title, message, exit_event: Incomplete | None = None) -> None: ...
    def closeEvent(self, event) -> None: ...
    def quit(self) -> None: ...
    def showEvent(self, event) -> None: ...

qt_resource_data: bytes
qt_resource_name: bytes
qt_resource_struct: bytes

def qInitResources() -> None: ...
def qCleanupResources() -> None: ...

from PySide6.QtCore import QObject
from _typeshed import Incomplete
from ok.capture.Capture import BaseWindowsCaptureMethod as BaseWindowsCaptureMethod
from ok.gui.Communicate import communicate as communicate
from ok.gui.util.Alert import alert_error as alert_error
from ok.util.Util import Handler as Handler, execute as execute, get_logger as get_logger, is_admin as is_admin

logger: Incomplete

class StartController(QObject):
    config: Incomplete
    exit_event: Incomplete
    handler: Incomplete
    start_timeout: Incomplete
    def __init__(self, app_config, exit_event) -> None: ...
    def start(self, task: Incomplete | None = None): ...
    def do_start(self, task: Incomplete | None = None) -> None: ...
    def check_device_error(self): ...
    @staticmethod
    def try_capture_a_frame(): ...

from PySide6.QtWidgets import QTabBar, QTabWidget, QWidget

class TabBar(QTabBar):
    def __init__(self, *args, **kwargs) -> None: ...
    def tabSizeHint(self, index): ...
    def paintEvent(self, event) -> None: ...

class VerticalTabWidget(QTabWidget):
    def __init__(self) -> None: ...

class TabContent(QWidget):
    def __init__(self, text) -> None: ...

from _typeshed import Incomplete
from ok.gui.about.VersionCard import VersionCard as VersionCard
from ok.gui.widget.Tab import Tab as Tab
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class AboutTab(Tab):
    version_card: Incomplete
    def __init__(self, config) -> None: ...
    def update_update_buttons(self) -> None: ...
    def update_update(self, error) -> None: ...

def text_to_html_paragraphs(text): ...

from _typeshed import Incomplete
from qfluentwidgets import TextEdit

class VersionCard(TextEdit):
    anchor: Incomplete
    def __init__(self, parent: Incomplete | None = None) -> None: ...
    def mousePressEvent(self, e) -> None: ...
    def mouseReleaseEvent(self, e) -> None: ...

from PySide6.QtCore import Qt as Qt
from _typeshed import Incomplete
from ok.gui.launcher.LinksBar import LinksBar as LinksBar
from ok.util.Util import get_logger as get_logger
from qfluentwidgets import SettingCard

logger: Incomplete

class VersionCard(SettingCard):
    def __init__(self, config, icon, title, version, debug, parent: Incomplete | None = None) -> None: ...
    def get_type(self, debug: Incomplete | None = None): ...

from _typeshed import Incomplete
from ok.gui.about.VersionCard import VersionCard as VersionCard
from ok.gui.widget.Tab import Tab as Tab
from ok.main.globals import og as og
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class ActTab(Tab):
    version_card: Incomplete
    def __init__(self, config) -> None: ...

from _typeshed import Incomplete
from enum import Enum
from ok.util.Util import get_relative_path as get_relative_path
from qfluentwidgets import ConfigSerializer, QConfig

class Language(Enum):
    CHINESE_SIMPLIFIED = ...
    ENGLISH = ...
    AUTO = ...

class LanguageSerializer(ConfigSerializer):
    def serialize(self, language): ...
    def deserialize(self, value: str): ...

def isWin11(): ...

class AppConfig(QConfig):
    micaEnabled: Incomplete
    dpiScale: Incomplete
    language: Incomplete
    blurRadius: Incomplete
    checkUpdateAtStartUp: Incomplete

cfg: Incomplete

from enum import Enum
from qfluentwidgets import FluentIconBase

class OKIcon(FluentIconBase, Enum):
    STOP = 'stop'
    DISCORD = 'discord'
    HEART = 'heart'
    def path(self, theme=...): ...

from enum import Enum
from qfluentwidgets import StyleSheetBase

class StyleSheet(StyleSheetBase, Enum):
    LINK_CARD = 'link_card'
    CARD = 'card'
    STATUS_BAR = 'status_bar'
    TAB = 'tab'
    MESSAGE_WINDOW = 'message_window'
    SETTING_INTERFACE = 'setting_interface'
    def path(self, theme=...): ...

from PySide6.QtCore import Signal
from _typeshed import Incomplete
from ok.capture.Capture import ImageCaptureMethod as ImageCaptureMethod
from ok.capture.windows.dump import dump_threads as dump_threads
from ok.config.Config import Config as Config
from ok.gui.i18n.GettextTranslator import convert_to_mo_files as convert_to_mo_files
from ok.gui.util.Alert import alert_error as alert_error, alert_info as alert_info
from ok.gui.widget.Tab import Tab as Tab
from ok.interaction.DoNothingInteraction import DoNothingInteraction as DoNothingInteraction
from ok.util.Util import Handler as Handler, exception_to_str as exception_to_str, get_logger as get_logger

logger: Incomplete

class DebugTab(Tab):
    update_result_text: Signal
    config: Incomplete
    log_window_config: Incomplete
    handler: Incomplete
    log_window: Incomplete
    select_screenshot_button: Incomplete
    tasks_combo_box: Incomplete
    target_function_edit: Incomplete
    call_button: Incomplete
    result_edit: Incomplete
    def __init__(self, app_config, exit_event) -> None: ...
    def toggle_log_window(self) -> None: ...
    def gen_tr(self) -> None: ...
    def check_hotkey(self) -> None: ...
    def bind_hot_keys(self) -> None: ...
    @staticmethod
    def unregister() -> None: ...
    def call(self) -> None: ...
    def ocr(self) -> None: ...
    def task_changed(self, text) -> None: ...
    def select_screenshot(self) -> None: ...

def capture() -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class FrameWidget(QWidget):
    timer: Incomplete
    mouse_font: Incomplete
    scaling: Incomplete
    def __init__(self) -> None: ...
    def update_mouse_position(self) -> None: ...
    def frame_ratio(self): ...
    def paintEvent(self, event) -> None: ...
    def paint_boxes(self, painter) -> None: ...
    def paint_border(self, painter) -> None: ...
    def paint_mouse_position(self, painter) -> None: ...

from PySide6.QtCore import QAbstractListModel
from PySide6.QtWidgets import QStyledItemDelegate, QWidget
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate

LOG_BG_TRANS: int
color_codes: Incomplete

class ColoredText:
    text: Incomplete
    format: Incomplete
    level: Incomplete
    def __init__(self, text, format, level) -> None: ...

class ColorDelegate(QStyledItemDelegate):
    def __init__(self, parent: Incomplete | None = None) -> None: ...
    def paint(self, painter, option, index) -> None: ...

class LogModel(QAbstractListModel):
    logs: Incomplete
    filtered_logs: Incomplete
    current_level: str
    current_keyword: str
    def __init__(self) -> None: ...
    def data(self, index, role): ...
    def rowCount(self, index): ...
    def add_log(self, level, message) -> None: ...
    def do_filter_logs(self) -> None: ...
    def filter_logs(self, level, keyword) -> None: ...
    def get_color_format(self, level): ...

log_levels: Incomplete
level_severity: Incomplete

class LogWindow(QWidget):
    floating: Incomplete
    config: Incomplete
    old_pos: Incomplete
    layout: Incomplete
    filter_layout: Incomplete
    log_list: Incomplete
    level_filter: Incomplete
    keyword_filter: Incomplete
    drag_button: Incomplete
    close_button: Incomplete
    log_model: Incomplete
    black_list_logs: Incomplete
    def __init__(self, config: Incomplete | None = None, floating: bool = True) -> None: ...
    def close(self) -> None: ...
    def add_log(self, level_no, message) -> None: ...
    def filter_logs(self) -> None: ...
    def mousePressEvent(self, event) -> None: ...
    def mouseMoveEvent(self, event) -> None: ...
    def mouseReleaseEvent(self, event) -> None: ...

from PySide6.QtCore import QObject
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import Box as Box, clear_folder as clear_folder, find_first_existing_file as find_first_existing_file, get_logger as get_logger, get_relative_path as get_relative_path, sanitize_filename as sanitize_filename

logger: Incomplete

class Screenshot(QObject):
    queue: Incomplete
    time_to_expire: int
    ui_dict: Incomplete
    color_map: Incomplete
    exit_event: Incomplete
    click_screenshot_folder: Incomplete
    screenshot_folder: Incomplete
    task_queue: Incomplete
    thread: Incomplete
    pil_font: Incomplete
    def __init__(self, exit_event) -> None: ...
    def screenshot(self, frame, name) -> None: ...
    def draw_box(self, key: str = None, boxes: Incomplete | None = None, color: str = 'red', frame: Incomplete | None = None): ...
    def remove_expired(self) -> None: ...
    def add_task(self, frame, folder, name: Incomplete | None = None) -> None: ...
    def generate_screen_shot(self, frame, ui_dict, folder, name): ...
    @staticmethod
    def save_pil_image(name, folder, pil_image): ...
    def stop(self) -> None: ...
    def to_pil_image(self, frame): ...

def get_current_time_formatted(): ...

from ok.util.Util import ensure_dir_for_file as ensure_dir_for_file, get_path_relative_to_exe as get_path_relative_to_exe, resource_path as resource_path

def update_po_file(strings, language_code): ...
def convert_to_mo_files() -> None: ...
def get_translations(language): ...

from _typeshed import Incomplete

i18n_path: Incomplete

from _typeshed import Incomplete

directory: str
extension: str
command: str
files: Incomplete
full_path: Incomplete
files_str: Incomplete

from _typeshed import Incomplete

script_dir: Incomplete
icon_path: Incomplete

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class DownloadBar(QWidget):
    hbox_layout: Incomplete
    download_bar: Incomplete
    downloading_text: Incomplete
    def __init__(self) -> None: ...
    def update_running(self, running) -> None: ...
    def update_buttons(self, downloading, downloaded, total, percent) -> None: ...

from _typeshed import Incomplete
from ok.gui.launcher.LauncherWindow import LauncherWindow as LauncherWindow
from ok.gui.util.app import center_window as center_window, init_app_config as init_app_config
from ok.update.GitUpdater import GitUpdater as GitUpdater
from ok.util.Util import ExitEvent as ExitEvent, config_logger as config_logger, get_logger as get_logger

logger: Incomplete

class Launcher:
    app: Incomplete
    locale: Incomplete
    config: Incomplete
    exit_event: Incomplete
    updater: Incomplete
    def __init__(self, config) -> None: ...
    def start(self) -> None: ...

from _typeshed import Incomplete
from ok.gui.common.style_sheet import StyleSheet as StyleSheet
from ok.gui.launcher.RunBar import RunBar as RunBar
from ok.gui.launcher.UpdateBar import UpdateBar as UpdateBar
from ok.gui.widget.BaseWindow import BaseWindow as BaseWindow
from ok.util.Util import get_logger as get_logger, get_path_relative_to_exe as get_path_relative_to_exe

logger: Incomplete

class LauncherWindow(BaseWindow):
    exit_event: Incomplete
    updater: Incomplete
    icon: Incomplete
    layout: Incomplete
    install_bar: Incomplete
    run_bar: Incomplete
    def __init__(self, config, updater, exit_event) -> None: ...
    def closeEvent(self, event) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.common.OKIcon import OKIcon as OKIcon
from ok.gui.util.Alert import alert_info as alert_info
from ok.gui.util.app import get_localized_app_config as get_localized_app_config
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class LinksBar(QWidget):
    link_config: Incomplete
    layout: Incomplete
    version_label: Incomplete
    github_button: Incomplete
    discord_button: Incomplete
    share_button: Incomplete
    sponsor_button: Incomplete
    def __init__(self, app_config) -> None: ...
    def share(self) -> None: ...
    def open_url(self, url_name) -> None: ...
    def get_url(self, url_name): ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.update.GitUpdater import GitUpdater as GitUpdater
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class RunBar(QWidget):
    updater: Incomplete
    profile_connected: bool
    layout: Incomplete
    version_label: Incomplete
    profile_layout: Incomplete
    profile_label: Incomplete
    profiles: Incomplete
    run_button: Incomplete
    def __init__(self, updater: GitUpdater) -> None: ...
    def update_version_label(self) -> None: ...
    def start_clicked(self) -> None: ...
    def profile_changed_clicked(self) -> None: ...
    def update_profile(self, profiles) -> None: ...
    def update_running(self, running) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.launcher.DownloadBar import DownloadBar as DownloadBar
from ok.gui.launcher.LinksBar import LinksBar as LinksBar
from ok.update.GitUpdater import GitUpdater as GitUpdater, is_newer_or_eq_version as is_newer_or_eq_version
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class UpdateBar(QWidget):
    updater: Incomplete
    layout: Incomplete
    version_log_label: Incomplete
    links_bar: Incomplete
    download_bar: Incomplete
    hbox_layout: Incomplete
    update_hbox_layout: Incomplete
    delete_dependencies_button: Incomplete
    update_source_box: Incomplete
    source_label: Incomplete
    update_sources: Incomplete
    check_update_button: Incomplete
    version_label: Incomplete
    version_label_target: Incomplete
    current_version: Incomplete
    version_list: Incomplete
    update_button: Incomplete
    def __init__(self, config, updater: GitUpdater) -> None: ...
    def update_source(self) -> None: ...
    def version_selection_changed(self, text) -> None: ...
    def update_update_btns(self, text) -> None: ...
    def update_logs(self, logs) -> None: ...
    def update_clicked(self) -> None: ...
    def update_running(self, running) -> None: ...
    def update_versions(self, versions) -> None: ...
    def set_op_btn_visible(self, visible) -> None: ...

from PySide6.QtCore import QObject
from _typeshed import Incomplete
from ok.capture.Capture import HwndWindow as HwndWindow
from ok.gui.debug.FrameWidget import FrameWidget as FrameWidget
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class Communicate(QObject):
    speak: Incomplete

class OverlayWindow(FrameWidget):
    def __init__(self, hwnd_window: HwndWindow) -> None: ...
    def update_overlay(self, visible, x, y, window_width, window_height, width, height, scaling) -> None: ...

from ok.config.Config import Config as Config
from ok.config.ConfigOption import ConfigOption as ConfigOption
from ok.gui.tasks.ConfigCard import ConfigCard as ConfigCard

class GlobalConfigCard(ConfigCard):
    def __init__(self, config: Config, option: ConfigOption) -> None: ...
    def reset_clicked(self) -> None: ...

from _typeshed import Incomplete
from ok.gui.common.config import cfg as cfg
from ok.gui.settings.GlobalConfigCard import GlobalConfigCard as GlobalConfigCard
from ok.gui.widget.Tab import Tab as Tab

class SettingTab(Tab):
    personalGroup: Incomplete
    languageCard: Incomplete
    app_group: Incomplete
    def __init__(self) -> None: ...
    def add_global_config(self) -> None: ...

from qfluentwidgets import ListWidget

class SelectCaptureListView(ListWidget):
    def __init__(self, index_change_callback) -> None: ...
    def update_for_device(self) -> None: ...
    def reduce_row_to_1(self) -> None: ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.debug.DebugTab import capture as capture
from ok.gui.widget.StatusBar import StatusBar as StatusBar
from ok.main.globals import og as og
from ok.util.Util import Handler as Handler, get_logger as get_logger
from qfluentwidgets import SettingCard

logger: Incomplete

class StartCard(SettingCard):
    show_choose_hwnd: Incomplete
    status_bar: Incomplete
    capture_button: Incomplete
    start_button: Incomplete
    handler: Incomplete
    def __init__(self, exit_event) -> None: ...
    def status_clicked(self) -> None: ...
    def clicked(self) -> None: ...
    def update_task(self, task) -> None: ...
    def update_status(self) -> None: ...
    def check_hotkey(self) -> None: ...
    def bind_hot_keys(self) -> None: ...

from PySide6.QtCore import Qt as Qt
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.start.SelectCaptureListView import SelectCaptureListView as SelectCaptureListView
from ok.gui.start.StartCard import StartCard as StartCard
from ok.gui.widget.Tab import Tab as Tab
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class StartTab(Tab):
    select_hwnd_window: Incomplete
    device_list_row: int
    capture_list_row: int
    start_card: Incomplete
    device_list: Incomplete
    device_container: Incomplete
    refresh_button: Incomplete
    capture_list: Incomplete
    interaction_container: Incomplete
    closed_by_finish_loading: bool
    message: str
    def __init__(self, exit_event) -> None: ...
    def update_window_list(self) -> None: ...
    def refresh_clicked(self) -> None: ...
    def capture_index_changed(self) -> None: ...
    def device_index_changed(self) -> None: ...
    def update_capture(self, finished) -> None: ...
    def update_selection(self) -> None: ...
    def update_progress(self, message) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigItemFactory import config_widget as config_widget
from qfluentwidgets import ExpandSettingCard

class ConfigCard(ExpandSettingCard):
    config: Incomplete
    config_widgets: Incomplete
    default_config: Incomplete
    config_description: Incomplete
    config_type: Incomplete
    reset_config: Incomplete
    def __init__(self, name, config, description, default_config, config_description, config_type, config_icon) -> None: ...
    def reset_clicked(self) -> None: ...
    def update_config(self) -> None: ...

from ok.gui.tasks.LabelAndDoubleSpinBox import LabelAndDoubleSpinBox as LabelAndDoubleSpinBox
from ok.gui.tasks.LabelAndDropDown import LabelAndDropDown as LabelAndDropDown
from ok.gui.tasks.LabelAndLineEdit import LabelAndLineEdit as LabelAndLineEdit
from ok.gui.tasks.LabelAndMultiSelection import LabelAndMultiSelection as LabelAndMultiSelection
from ok.gui.tasks.LabelAndSpinBox import LabelAndSpinBox as LabelAndSpinBox
from ok.gui.tasks.LabelAndSwitchButton import LabelAndSwitchButton as LabelAndSwitchButton
from ok.gui.tasks.ModifyListItem import ModifyListItem as ModifyListItem

def config_widget(config_type, config_desc, config, key, value): ...

from _typeshed import Incomplete
from ok.gui.tasks.LabelAndWidget import LabelAndWidget as LabelAndWidget

class ConfigLabelAndWidget(LabelAndWidget):
    key: Incomplete
    config: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_config(self, value) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget

class LabelAndDoubleSpinBox(ConfigLabelAndWidget):
    key: Incomplete
    spin_box: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_value(self) -> None: ...
    def value_changed(self, value) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget
from ok.util.Util import find_index_in_list as find_index_in_list

class LabelAndDropDown(ConfigLabelAndWidget):
    key: Incomplete
    tr_dict: Incomplete
    tr_options: Incomplete
    combo_box: Incomplete
    def __init__(self, config_desc, options, config, key: str) -> None: ...
    def text_changed(self, text) -> None: ...
    def update_value(self) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget

class LabelAndLineEdit(ConfigLabelAndWidget):
    key: Incomplete
    line_edit: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_value(self) -> None: ...
    def value_changed(self, value) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget

class LabelAndDoubleSpinBox(ConfigLabelAndWidget):
    key: Incomplete
    config: Incomplete
    spin_box: Incomplete
    def __init__(self, config, config_desc, key: str) -> None: ...
    def value_changed(self, value) -> None: ...

from PySide6.QtCore import Qt as Qt
from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget
from ok.gui.widget.FlowLayout import FlowLayout as FlowLayout

class LabelAndMultiSelection(ConfigLabelAndWidget):
    key: Incomplete
    tr_dict: Incomplete
    tr_options: Incomplete
    user_action: bool
    content_layout: Incomplete
    check_boxes: Incomplete
    def __init__(self, config_desc, options, config, key: str) -> None: ...
    def check_changed(self, checked) -> None: ...
    def update_value(self) -> None: ...

class CheckBoxWidget(QWidget):
    def __init__(self, options) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget

class LabelAndSpinBox(ConfigLabelAndWidget):
    key: Incomplete
    spin_box: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_value(self) -> None: ...
    def value_changed(self, value) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget

class LabelAndSwitchButton(ConfigLabelAndWidget):
    key: Incomplete
    switch_button: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_value(self) -> None: ...
    def check_changed(self, checked) -> None: ...

from PySide6.QtWidgets import QLayout, QWidget
from _typeshed import Incomplete

class LabelAndWidget(QWidget):
    layout: Incomplete
    title_layout: Incomplete
    title: Incomplete
    contentLabel: Incomplete
    def __init__(self, title: str, content: Incomplete | None = None) -> None: ...
    def add_widget(self, widget: QWidget, stretch: int = 0): ...
    def add_layout(self, layout: QLayout, stretch: int = 0): ...

from _typeshed import Incomplete
from qfluentwidgets import MessageBoxBase

class ModifyListDialog(MessageBoxBase):
    list_modified: Incomplete
    titleLabel: Incomplete
    original_items: Incomplete
    list_widget: Incomplete
    move_up_button: Incomplete
    move_down_button: Incomplete
    add_button: Incomplete
    remove_button: Incomplete
    def __init__(self, items, parent) -> None: ...
    def move_up(self) -> None: ...
    def move_down(self) -> None: ...
    def add_item(self) -> None: ...
    def remove_item(self) -> None: ...
    def confirm(self) -> None: ...
    def cancel(self) -> None: ...

class AddTextMessageBox(MessageBoxBase):
    titleLabel: Incomplete
    add_text_edit: Incomplete
    def __init__(self, parent: Incomplete | None = None) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.ConfigLabelAndWidget import ConfigLabelAndWidget as ConfigLabelAndWidget
from ok.gui.tasks.ModifyListDialog import ModifyListDialog as ModifyListDialog
from ok.gui.widget.UpdateConfigWidgetItem import value_to_string as value_to_string

class ModifyListItem(ConfigLabelAndWidget):
    switch_button: Incomplete
    list_text: Incomplete
    def __init__(self, config_desc, config, key: str) -> None: ...
    def update_value(self) -> None: ...
    def clicked(self) -> None: ...
    def list_modified(self, the_list) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.TaskCard import TaskCard as TaskCard
from ok.gui.tasks.TaskTab import TaskTab as TaskTab
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class OneTimeTaskTab(TaskTab):
    keep_info_when_done: bool
    def __init__(self) -> None: ...
    def in_current_list(self, task): ...

from PySide6.QtWidgets import QPushButton as QPushButton
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.util.Alert import show_alert as show_alert
from ok.util.Util import get_logger as get_logger
from qfluentwidgets import PushButton

logger: Incomplete

class StartButton(PushButton):
    animation: Incomplete
    def __init__(self) -> None: ...
    def update_paused(self, paused) -> None: ...
    def toggle_text(self) -> None: ...
    def start_animation(self) -> None: ...

from PySide6.QtCore import Qt as Qt
from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.common.OKIcon import OKIcon as OKIcon
from ok.gui.tasks.ConfigCard import ConfigCard as ConfigCard
from ok.task.Task import BaseTask as BaseTask

class TaskCard(ConfigCard):
    task: Incomplete
    onetime: Incomplete
    task_buttons: Incomplete
    enable_button: Incomplete
    def __init__(self, task: BaseTask, onetime) -> None: ...
    def start_clicked(self) -> None: ...
    def update_buttons(self, task) -> None: ...
    def check_changed(self, checked) -> None: ...

class TaskButtons(QWidget):
    task: Incomplete
    def __init__(self, task) -> None: ...
    layout: Incomplete
    start_button: Incomplete
    stop_button: Incomplete
    pause_button: Incomplete
    def init_ui(self) -> None: ...
    def toggle_button_visibility(self, button, visible) -> None: ...
    def adjust_spacing(self) -> None: ...
    def update_buttons(self) -> None: ...
    def start_clicked(self) -> None: ...
    def stop_clicked(self) -> None: ...
    def pause_clicked(self) -> None: ...

from PySide6.QtWidgets import QPushButton
from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class TaskOpButton(QPushButton):
    task: Incomplete
    def __init__(self, task: BaseTask) -> None: ...
    def update_task(self, task: BaseTask): ...
    def toggle_text(self) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.TooltipTableWidget import TooltipTableWidget as TooltipTableWidget
from ok.gui.widget.Tab import Tab as Tab
from ok.gui.widget.UpdateConfigWidgetItem import value_to_string as value_to_string
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class TaskTab(Tab):
    keep_info_when_done: bool
    current_task_name: str
    last_task: Incomplete
    task_info_table: Incomplete
    task_info_container: Incomplete
    task_info_labels: Incomplete
    timer: Incomplete
    def __init__(self) -> None: ...
    def in_current_list(self, task): ...
    @staticmethod
    def time_elapsed(start_time): ...
    def update_info_table(self) -> None: ...
    def update_task_info(self, task) -> None: ...
    def uneditable_item(self): ...

from _typeshed import Incomplete
from qfluentwidgets import TableWidget

class TooltipTableWidget(TableWidget):
    width_percentages: Incomplete
    def __init__(self, width_percentages: Incomplete | None = None) -> None: ...
    def resizeEvent(self, event) -> None: ...

from _typeshed import Incomplete
from ok.gui.tasks.TaskCard import TaskCard as TaskCard
from ok.gui.tasks.TaskTab import TaskTab as TaskTab
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class TriggerTaskTab(TaskTab):
    def __init__(self) -> None: ...
    def in_current_list(self, task): ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import get_logger as get_logger

logger: Incomplete

def show_alert(title, message) -> None: ...
def alert_info(message, tray: bool = False) -> None: ...
def alert_error(message, tray: bool = False) -> None: ...

from _typeshed import Incomplete
from ok.gui import resources as resources
from ok.gui.common.config import cfg as cfg
from ok.util.Util import get_logger as get_logger

logger: Incomplete

def init_app_config(): ...
def get_localized_app_config(config, key): ...
def show_info_bar(window, message, title: Incomplete | None = None, error: bool = False) -> None: ...
def center_window(app, window) -> None: ...

from PySide6.QtCore import QThread
from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class InitWorker(QThread):
    fun: Incomplete
    def __init__(self, fun) -> None: ...
    def run(self) -> None: ...

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

def get_installed_packages(pip_command): ...
def get_package_required_by(package_name, pip_command): ...
def uninstall_packages(packages, pip_command) -> None: ...
def get_package_dependencies(packages, pip_command): ...
def get_all_dependencies(packages, pip_command): ...
def clean_packages(to_install, pip_command) -> None: ...
def parse_package_names(package_string): ...
def build_reverse_map(dependency_map): ...
def is_required_by(package, package_to_parents, to_install): ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.util.Alert import alert_error as alert_error
from ok.gui.widget.BaseWindow import BaseWindow as BaseWindow
from ok.main.globals import og as og
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class ActWindow(BaseWindow):
    result_event: Incomplete
    user_closed: bool
    vbox: Incomplete
    key_input: Incomplete
    uid_input: Incomplete
    activate_btn: Incomplete
    def __init__(self, icon: Incomplete | None = None) -> None: ...
    def activate(self) -> None: ...
    def on_result(self, success, message) -> None: ...
    def do_check_auth(self) -> None: ...
    def closeEvent(self, event) -> None: ...
    def showEvent(self, event) -> None: ...

from _typeshed import Incomplete
from ok.gui.widget.StartLoadingDialog import StartLoadingDialog as StartLoadingDialog

class BaseLoading:
    loading_dialog: Incomplete
    def __init__(self) -> None: ...
    def show_loading(self, message: str = '') -> None: ...
    def close_loading(self) -> None: ...

from PySide6.QtCore import QRect, QSize
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.gui.util.app import show_info_bar as show_info_bar
from ok.gui.widget.BaseLoading import BaseLoading as BaseLoading
from ok.main.globals import og as og
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

class BaseWindow(BackgroundAnimationWidget, FramelessWindow, BaseLoading):
    def __init__(self, parent: Incomplete | None = None) -> None: ...
    def setCustomBackgroundColor(self, light, dark) -> None: ...
    def paintEvent(self, e) -> None: ...
    def setMicaEffectEnabled(self, isEnabled: bool): ...
    def show_notification(self, message, title: Incomplete | None = None, error: bool = False, tray: bool = False) -> None: ...
    def isMicaEffectEnabled(self): ...
    def systemTitleBarRect(self, size: QSize) -> QRect: ...
    def setTitleBar(self, titleBar) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.common.style_sheet import StyleSheet as StyleSheet

class Card(QWidget):
    widget: Incomplete
    stretch: Incomplete
    title_layout: Incomplete
    titleLabel: Incomplete
    card: Incomplete
    vBoxLayout: Incomplete
    cardLayout: Incomplete
    topLayout: Incomplete
    def __init__(self, title, widget, stretch: int = 0, parent: Incomplete | None = None) -> None: ...
    def add_top_widget(self, widget) -> None: ...

from _typeshed import Incomplete
from ok.gui.widget.Tab import Tab as Tab
from ok.task.Task import TaskExecutor as TaskExecutor

class CustomTab(Tab):
    executor: Incomplete
    def __init__(self) -> None: ...
    def get_task(self, cls): ...
    @property
    def name(self): ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.common.style_sheet import StyleSheet as StyleSheet

class EmptyCard(QWidget):
    card: Incomplete
    def __init__(self, layout, parent: Incomplete | None = None) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete

class FlowLayout(QWidget):
    vbox: Incomplete
    def __init__(self) -> None: ...
    hbox: Incomplete
    current_width: int
    def add_new_hbox(self) -> None: ...
    def add_widget(self, widget) -> None: ...

from PySide6.QtWidgets import QDialog
from _typeshed import Incomplete
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

class FramelessDialog(QDialog, FramelessWindow):
    def __init__(self, parent: Incomplete | None = None) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.main.globals import og as og

class ImageWidget(QWidget):
    cache: Incomplete
    image: Incomplete
    def __init__(self, image_path, parent: Incomplete | None = None) -> None: ...
    def paintEvent(self, event) -> None: ...
    @staticmethod
    def check_exist(image_path): ...

from PySide6.QtWidgets import QTableWidgetItem
from _typeshed import Incomplete
from ok.gui.widget.UpdateConfigWidgetItem import UpdateConfigWidgetItem as UpdateConfigWidgetItem, value_to_string as value_to_string

class ListTableWidgetItem(UpdateConfigWidgetItem, QTableWidgetItem):
    def __init__(self, config, key, value, parent: Incomplete | None = None) -> None: ...
    def setData(self, role, value) -> None: ...

def convert_to_list(s): ...

from PySide6.QtWidgets import QTableWidgetItem
from _typeshed import Incomplete
from ok.gui.widget.UpdateConfigWidgetItem import UpdateConfigWidgetItem as UpdateConfigWidgetItem, value_to_string as value_to_string

class NumericTableWidgetItem(UpdateConfigWidgetItem, QTableWidgetItem):
    validator: Incomplete
    def __init__(self, config, key, value, parent: Incomplete | None = None) -> None: ...
    def setData(self, role, value) -> None: ...

from qfluentwidgets.components.widgets.spin_box import CompactSpinBox

class OkCompactSpinBox(CompactSpinBox):
    def __init__(self, *args, **kwargs) -> None: ...
    def focusInEvent(self, e) -> None: ...

from qfluentwidgets import PrimaryPushButton

class RedPrimaryPushButton(PrimaryPushButton):
    def __init__(self, *args, **kwargs) -> None: ...

from PySide6.QtWidgets import QTableWidgetItem
from _typeshed import Incomplete

class SortingTableWidgetItem(QTableWidgetItem):
    def __init__(self, name: Incomplete | None = None) -> None: ...
    def __lt__(self, other): ...
    @staticmethod
    def convert_to_float(value): ...

from _typeshed import Incomplete
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase

class StartLoadingDialog(MaskDialogBase):
    seconds_left: Incomplete
    vBoxLayout: Incomplete
    spinner: Incomplete
    loading_label: Incomplete
    timer: Incomplete
    def __init__(self, seconds_left: int, parent: Incomplete | None = None) -> None: ...
    def set_seconds_left(self, seconds_left: int): ...
    def update_countdown(self) -> None: ...
    def close(self) -> None: ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete
from ok.gui.common.style_sheet import StyleSheet as StyleSheet

class StatusBar(QWidget):
    clicked: Incomplete
    title: Incomplete
    titleLabel: Incomplete
    rotateTimer: Incomplete
    opacityEffect: Incomplete
    animation: Incomplete
    isDone: Incomplete
    rotateAngle: int
    deltaAngle: int
    running_icon: Incomplete
    done_icon: Incomplete
    def __init__(self, title, running_icon=..., done_icon=..., done: bool = True, parent: Incomplete | None = None) -> None: ...
    def mousePressEvent(self, event) -> None: ...
    def setTitle(self, title: str): ...
    def setState(self, isDone: bool = False) -> None: ...
    def getSuitablePos(self): ...
    def paintEvent(self, e) -> None: ...

from _typeshed import Incomplete
from ok.gui.common.style_sheet import StyleSheet as StyleSheet
from ok.gui.widget.Card import Card as Card
from ok.gui.widget.StartLoadingDialog import StartLoadingDialog as StartLoadingDialog
from qfluentwidgets import ScrollArea

class Tab(ScrollArea):
    loading_dialog: Incomplete
    view: Incomplete
    vBoxLayout: Incomplete
    def __init__(self) -> None: ...
    @property
    def exit_event(self): ...
    def show_loading_dialog(self) -> None: ...
    def hide_loading_dialog(self) -> None: ...
    def addCard(self, title, widget, stretch: int = 0, parent: Incomplete | None = None): ...
    def addWidget(self, *args, **kwargs) -> None: ...
    def addLayout(self, layout, stretch: int = 0): ...

from PySide6.QtWidgets import QWidget

class TabWidget(QWidget):
    def __init__(self) -> None: ...
    def get_palette_color(self, palette_color): ...

def color_to_hex(color): ...

from _typeshed import Incomplete

class UpdateConfigWidgetItem:
    key: Incomplete
    config: Incomplete
    value: Incomplete
    def __init__(self, config, key, value) -> None: ...
    def set_value(self, value) -> None: ...

def value_to_string(obj): ...

from PySide6.QtWidgets import QWidget
from _typeshed import Incomplete

class WidgetWithVLabel(QWidget):
    layout: Incomplete
    label: Incomplete
    def __init__(self, title, widget: QWidget, parent: Incomplete | None = None) -> None: ...
    def set_label(self, label) -> None: ...

from PySide6.QtWidgets import QComboBox
from ok.gui.widget.UpdateConfigWidgetItem import UpdateConfigWidgetItem as UpdateConfigWidgetItem

class YesNonWidgetItem(UpdateConfigWidgetItem, QComboBox):
    def __init__(self, config, key, value) -> None: ...
    def index_changed(self, index) -> None: ...

from _typeshed import Incomplete
from ok.interaction.BaseInteraction import BaseInteraction as BaseInteraction
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class ADBBaseInteraction(BaseInteraction):
    device_manager: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, device_manager, capture, device_width, device_height) -> None: ...
    def send_key(self, key, down_time: float = 0.02) -> None: ...
    def swipe(self, from_x, from_y, to_x, to_y, duration, settle_time: float = 0.1) -> None: ...
    def click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, down_time: float = 0.01, move: bool = True) -> None: ...

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class BaseInteraction:
    capture: Incomplete
    def __init__(self, capture) -> None: ...
    def should_capture(self): ...
    def send_key(self, key, down_time: float = 0.02) -> None: ...
    def send_key_down(self, key) -> None: ...
    def send_key_up(self, key) -> None: ...
    def move(self, x, y) -> None: ...
    def swipe(self, from_x, from_y, to_x, to_y, duration, settle_time) -> None: ...
    def middle_click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, down_time: float = 0.05) -> None: ...
    def click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, move=..., down_time: float = 0.05) -> None: ...
    def right_click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None) -> None: ...
    def on_run(self) -> None: ...

from _typeshed import Incomplete
from ok.interaction.BaseInteraction import BaseInteraction as BaseInteraction
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class DoNothingInteraction(BaseInteraction): ...

from _typeshed import Incomplete
from ok.capture.Capture import BaseCaptureMethod as BaseCaptureMethod
from ok.interaction.BaseInteraction import BaseInteraction as BaseInteraction
from ok.util.Util import get_logger as get_logger

logger: Incomplete

class PostMessageInteraction(BaseInteraction):
    hwnd_window: Incomplete
    mouse_pos: Incomplete
    last_activate: int
    activate_interval: int
    def __init__(self, capture: BaseCaptureMethod, hwnd_window) -> None: ...
    @property
    def hwnd(self): ...
    def send_key(self, key, down_time: float = 0.01) -> None: ...
    def send_key_down(self, key) -> None: ...
    def send_key_up(self, key) -> None: ...
    def get_key_by_str(self, key): ...
    def move(self, x, y, down_btn: int = 0) -> None: ...
    def middle_click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, down_time: float = 0.01) -> None: ...
    def scroll(self, x, y, scroll_amount) -> None: ...
    def post(self, message, wParam: int = 0, lParam: int = 0) -> None: ...
    def swipe(self, x1, y1, x2, y2, duration: int = 3, settle_time: float = 0.1) -> None: ...
    def activate(self) -> None: ...
    def try_activate(self) -> None: ...
    def click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, down_time: float = 0.01, move: bool = True) -> None: ...
    def right_click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None) -> None: ...
    def mouse_down(self, x: int = -1, y: int = -1, name: Incomplete | None = None, key: str = 'left') -> None: ...
    def update_mouse_pos(self, x, y, activate: bool = True): ...
    def mouse_up(self, key: str = 'left') -> None: ...
    def should_capture(self): ...

vk_key_dict: Incomplete

from _typeshed import Incomplete
from ok.capture.Capture import BaseCaptureMethod as BaseCaptureMethod
from ok.interaction.BaseInteraction import BaseInteraction as BaseInteraction
from ok.util.Util import get_logger as get_logger, is_admin as is_admin

logger: Incomplete

class PyDirectInteraction(BaseInteraction):
    hwnd_window: Incomplete
    def __init__(self, capture: BaseCaptureMethod, hwnd_window) -> None: ...
    def send_key(self, key, down_time: float = 0.01) -> None: ...
    def send_key_down(self, key) -> None: ...
    def send_key_up(self, key) -> None: ...
    def move(self, x, y) -> None: ...
    def swipe(self, x1, y1, x2, y2, duration, settle_time: float = 0.1) -> None: ...
    def click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None, down_time: float = 0.01, move: bool = False) -> None: ...
    def right_click(self, x: int = -1, y: int = -1, move_back: bool = False, name: Incomplete | None = None) -> None: ...
    def mouse_down(self, x: int = -1, y: int = -1, name: Incomplete | None = None, key: str = 'left') -> None: ...
    def get_mouse_button(self, key): ...
    def mouse_up(self, key: str = 'left') -> None: ...
    def should_capture(self): ...
    def on_run(self) -> None: ...

import threading
from _typeshed import Incomplete

class LogTailer(threading.Thread):
    file_path: Incomplete
    stop_event: Incomplete
    exit_event: Incomplete
    listener: Incomplete
    file_descriptor: Incomplete
    def __init__(self, file_path, exit_event, listener) -> None: ...
    def run(self) -> None: ...
    def stop(self) -> None: ...

def get_log_level_number(log_message): ...

from _typeshed import Incomplete
from ok.util.Util import get_logger as get_logger, get_path_relative_to_exe as get_path_relative_to_exe

logger: Incomplete

class OkGlobals:
    app: Incomplete
    executor: Incomplete
    device_manager: Incomplete
    handler: Incomplete
    auth_uid: Incomplete
    auth_rd: Incomplete
    auth_expire: int
    my_app: Incomplete
    dpi_scaling: float
    app_path: Incomplete
    def __init__(self) -> None: ...
    def get_expire_util_str(self): ...
    def set_dpi_scaling(self, window) -> None: ...

og: Incomplete

import sys
import threading
import time
import ok
from ok.util.Util import get_logger, config_logger
from ok.util.Util import ExitEvent
from ok.util.Util import check_mutex
from ok.util.Util import install_path_isascii

class OK:

  def __init__(self, config):
    ...

  def app(self):
    ...

  def start(self):
    ...

  def do_init(self):
    ...

  def wait_task(self):
    ...

  def console_handler(self, event):
    ...

  def quit(self):
    ...

  def init_device_manager(self):
    ...

import ctypes
import sys
import threading

import time
from typing import List
import cv2
import numpy as np
from PySide6.QtCore import QCoreApplication
from ok.capture.Capture import CaptureException
from ok.util.Util import calculate_color_percentage
from ok.config.Config import Config
from ok.config.ConfigOption import ConfigOption
from ok.util.Util import (
	Box,
	sort_boxes,
	relative_box,
	find_boxes_by_name,
	find_highest_confidence_box
)
from ok.util.Util import find_box_by_name
from ok.feature.FeatureSet import adjust_coordinates
from ok.gui.Communicate import communicate
from ok.util.Util import get_logger
from ok.util.Util import Handler
from ok.util.Util import init_class_by_name
from ok.util.Util import ratio_text_to_number

class BaseTask(FindFeature):

  ...

class TaskDisabledException(Exception):

  ...

class CannotFindException(Exception):

  ...

class FinishedException(Exception):

  ...

class WaitFailedException(Exception):

  ...

class TaskExecutor:

  def sleep(self, timeout: float):
    """
          Sleeps for the specified timeout, checking for an exit event every 100ms, with adjustments to prevent oversleeping.

          :param timeout: The total time to sleep in seconds.
          """
    ...

def pause(self, task=None):
  ...

def start(self):
  ...

def wait_condition(self,
  condition,
  time_out=0,
  pre_action=None,
  post_action=None,
  wait_until_before_delay=-1,
  wait_until_check_delay=-1,
  raise_if_not_found=False):
  ...

def reset_scene(self):
  ...

def next_task(self) -> tuple:
  ...

def active_trigger_task_count(self):
  ...

def execute(self):
  ...

def stop(self):
  ...

def wait_until_done(self):
  ...

def get_all_tasks(self):
  ...

def get_task_by_class_name(self, class_name):
  ...

def get_task_by_class(self, cls):
  ...

def list_or_obj_to_str(val):
  ...

def prevent_sleeping(yes=True):
  ...

class ExecutorOperation:

  def __init__(self, executor: TaskExecutor):
    ...

def check_interval(self, interval):
  ...

def mouse_down(self, x=-1, y=-1, name=None, key="left"):
  ...

def mouse_up(self, name=None, key="left"):
  ...

def right_click(self, x=-1, y=-1, move_back=False, name=None):
  ...

def swipe_relative(self, from_x, from_y, to_x, to_y, duration=0.5):
  ...

def hwnd(self):
  ...

def scroll_relative(self, x, y, count):
  ...

def scroll(self, x, y, count):
  ...

def swipe(self, from_x, from_y, to_x, to_y, duration=0.5, settle_time=0.1):
  ...

def screenshot(self, name=None, frame=None):
  ...

def click_box_if_name_match(self, boxes, names, relative_x=0.5, relative_y=0.5):
  """
        Clicks on a box from a list of boxes if the box's name matches one of the specified names.
        The box to click is selected based on the order of names provided, with priority given
        to the earliest match in the names list.

        Parameters:
        - boxes (list): A list of box objects. Each box object must have a 'name' attribute.
        - names (str or list): A string or a list of strings representing the name(s) to match against the boxes' names.
        - relative_x (float, optional): The relative X coordinate within the box to click,
                                        as a fraction of the box's width. Defaults to 0.5 (center).
        - relative_y (float, optional): The relative Y coordinate within the box to click,
                                        as a fraction of the box's height. Defaults to 0.5 (center).

        Returns:
        - box: the matched box

        The method attempts to find and click on the highest-priority matching box. If no matches are found,
        or if there are no boxes, the method returns False. This operation is case-sensitive.
        """
  ...

def box_of_screen(self, x, y, to_x=1.0, to_y=1.0, width=0.0, height=0.0, name=None, hcenter=False):
  ...

def out_of_ratio(self):
  ...

def box_of_screen_scaled(self,
  original_screen_width,
  original_screen_height,
  x_original,
  y_original,
  to_x=0,
  to_y=0,
  width_original=0,
  height_original=0,
  name=None,
  hcenter=False):
  ...

def height_of_screen(self, percent):
  ...

def screen_width(self):
  ...

def screen_height(self):
  ...

def width_of_screen(self, percent):
  ...

def click_relative(self, x, y, move_back=False, hcenter=False, move=True, after_sleep=0, name=None):
  ...

def middle_click_relative(self, x, y, move_back=False, down_time=0.01):
  ...

def height(self):
  ...

def width(self):
  ...

def move_relative(self, x, y):
  ...

def move(self, x, y):
  ...

def wait_scene(self, scene_type=None, time_out=0, pre_action=None, post_action=None):
  ...

def sleep(self, timeout):
  ...

def send_key(self, key, down_time=0.02, interval=-1, after_sleep=0):
  ...

def get_global_config(self, option: ConfigOption):
  ...

def send_key_down(self, key):
  ...

def send_key_up(self, key):
  ...

def wait_until(self,
  condition,
  time_out=0,
  pre_action=None,
  post_action=None,
  wait_until_before_delay=-1,
  wait_until_check_delay=-1,
  raise_if_not_found=False):
  ...

def wait_click_box(self, condition, time_out=0, pre_action=None, post_action=None, raise_if_not_found=False):
  ...

def next_frame(self):
  ...

def scene(self):
  ...

def frame(self):
  ...

def draw_boxes(feature_name=None, boxes=None, color="red"):
  ...

def calculate_color_percentage(self, color, box: Box):
  ...

def adb_shell(self, *args, **kwargs):
  ...

class TriggerTask(BaseTask):

  ...

class FindFeature(OCR):

  def __init__(self, executor: TaskExecutor):
    ...

class OCR(ExecutorOperation):
  """
    Optical Character Recognition (OCR) class for detecting and recognizing text within images.

    Attributes:
        ocr_default_threshold (float): The default confidence threshold for OCR results.
        ocr_target_height (int): The target height for resizing images before OCR.
        text_fix (dict): A dictionary for fixing recognized text.
    """

  def __init__(self, executor: TaskExecutor):
    ...

def add_text_fix(self, fix):
  """Adds text fixes to the text_fix dictionary."""
  ...

def resize_image(image: object, original_height: int, target_height: int) -> tuple:
  """Resizes the image if the original height is significantly larger than the target height."""
  ...

def scale_box(box: object, scale_factor: float) -> void:
  """Scales the box coordinates by the given scale factor."""
  ...

def find_and_copy_site_package(): ...

import threading
from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import bytes_to_readable_size as bytes_to_readable_size, get_folder_size as get_folder_size, get_logger as get_logger

logger: Incomplete

class DownloadMonitor(threading.Thread):
    folder_path: Incomplete
    target_size: Incomplete
    stop_event: Incomplete
    exit_event: Incomplete
    size_from_log: int
    last_size: int
    size_from_file: int
    def __init__(self, folder_path, target_size, exit_event) -> None: ...
    def run(self) -> None: ...
    def notify(self) -> None: ...
    def update_running(self, running) -> None: ...
    def start_monitoring(self) -> None: ...
    def stop_monitoring(self) -> None: ...
    def handle_log(self, level_no, message) -> None: ...

def convert_to_bytes(size_str): ...

from ok.util.Util import delete_if_exists as delete_if_exists, dir_checksum as dir_checksum

def write_checksum_to_file(folder_path) -> None: ...

from _typeshed import Incomplete
from ok.gui.Communicate import communicate as communicate
from ok.util.Util import get_logger as get_logger

logger: Incomplete
download_url_us: Incomplete
download_url: Incomplete

def parse_url(urls): ...

class GithubMultiDownloader:
    app_config: Incomplete
    exit_event: Incomplete
    proxys: Incomplete
    fast_proxys: Incomplete
    lock: Incomplete
    num_parts: int
    downloaded: int
    start_time: int
    size: int
    def __init__(self, app_config, exit_event) -> None: ...
    def next_url(self, url): ...
    def download_part(self, part_size, start, end, file, giturl, last_proxy: Incomplete | None = None) -> None: ...
    def download(self, dir, release): ...
    def get_part_name(self, update_dir, i, release): ...

def convert_size(size_bytes): ...

from _typeshed import Incomplete
from ok.config.Config import Config as Config
from ok.gui.Communicate import communicate as communicate
from ok.gui.util.Alert import alert_error as alert_error, alert_info as alert_info
from ok.logging.LogTailer import LogTailer as LogTailer
from ok.update.DownloadMonitor import DownloadMonitor as DownloadMonitor
from ok.update.python_env import create_venv as create_venv, find_line_in_requirements as find_line_in_requirements, get_env_path as get_env_path, modify_venv_cfg as modify_venv_cfg
from ok.util.Util import Handler as Handler, delete_folders_starts_with as delete_folders_starts_with, delete_if_exists as delete_if_exists, get_logger as get_logger, get_relative_path as get_relative_path

logger: Incomplete
repo_path: Incomplete

class GitUpdater:
    exit_event: Incomplete
    app_config: Incomplete
    config: Incomplete
    debug: Incomplete
    lts_ver: str
    cuda_version: Incomplete
    launch_profiles: Incomplete
    all_versions: Incomplete
    launcher_config: Incomplete
    starting_version: Incomplete
    version_to_hash: Incomplete
    log_tailer: Incomplete
    yanked: bool
    outdated: bool
    auto_started: bool
    download_monitor: Incomplete
    handler: Incomplete
    launcher_configs: Incomplete
    app_env_path: Incomplete
    launcher_updated: bool
    def __init__(self, app_config, exit_event) -> None: ...
    @property
    def url(self): ...
    def update_launcher(self) -> None: ...
    def do_update_launcher(self) -> None: ...
    def kill_launcher(self) -> None: ...
    def load_current_ver(self) -> None: ...
    def log_handler(self, level, message) -> None: ...
    def get_current_profile(self): ...
    def update_source(self, index) -> None: ...
    def start_app(self): ...
    def version_selection_changed(self, new_version): ...
    def do_version_selection_changed(self, new_version) -> None: ...
    def install_package(self, package_name, app_env_path): ...
    def update_to_version(self, version): ...
    def read_launcher_config(self, path) -> None: ...
    def uninstall_dependencies(self, app_env_path, to_uninstall): ...
    def install_dependencies(self, env): ...
    def clear_dependencies(self) -> None: ...
    def do_clear_dependencies(self) -> None: ...
    def run(self) -> None: ...
    def do_run(self) -> None: ...
    def set_start_success(self) -> None: ...
    def check_out_version(self, version, depth: int = 10): ...
    def do_update_to_version(self, version) -> None: ...
    def list_all_versions(self) -> None: ...
    def do_list_all_versions(self): ...
    def change_profile(self, index) -> None: ...
    def auto_start(self): ...
    def get_sources(self): ...
    def get_default_source(self): ...
    def get_current_source(self): ...

def get_file_in_path_or_cwd(path, file): ...
def is_valid_version(tag): ...
def is_valid_repo(path): ...
def check_repo(path, new_url): ...
def move_file(src, dst_folder) -> None: ...
def format_date(date): ...
def is_newer_or_eq_version(v1, v2): ...
def get_updater_exe_local(): ...
def decode_and_clean(byte_string): ...
def get_version_text(lts, version, date, logs): ...
def wait_kill_pid(pid) -> None: ...
def kill_process_by_path(exe_path) -> None: ...
def clean_repo(repo_path, whitelist) -> None: ...
def copy_exe_files(folder1, folder2) -> None: ...
def fix_version_in_repo(repo_dir, tag) -> None: ...
def replace_ok_script_ver(content, full_version): ...
def add_to_path(folder_path) -> None: ...
def get_cuda_version(): ...

from _typeshed import Incomplete
from ok.update.GitUpdater import replace_ok_script_ver as replace_ok_script_ver
from ok.update.python_env import create_venv as create_venv, delete_files as delete_files, find_line_in_requirements as find_line_in_requirements
from ok.util.Util import config_logger as config_logger, get_logger as get_logger

logger: Incomplete

def replace_string_in_file(file_path, old_pattern, new_string) -> None: ...
def create_app_env(code_dir, build_dir, dependencies): ...
def create_launcher_env(code_dir: str = '.', build_dir: str = '.'): ...

from _typeshed import Incomplete
from ok.update.init_launcher_env import create_app_env as create_app_env
from ok.util.Util import config_logger as config_logger, delete_if_exists as delete_if_exists, get_logger as get_logger

logger: Incomplete

from _typeshed import Incomplete
from ok.config.Config import Config as Config
from ok.update.GitUpdater import copy_exe_files as copy_exe_files, fix_version_in_repo as fix_version_in_repo
from ok.update.init_launcher_env import create_launcher_env as create_launcher_env
from ok.util.Util import config_logger as config_logger, delete_if_exists as delete_if_exists, dir_checksum as dir_checksum, get_logger as get_logger

logger: Incomplete

def write_checksum_to_file(folder_path) -> None: ...
def get_git_exe_location(): ...

def run_command(command): ...
def on_rm_error(func, path, exc_info) -> None: ...
def get_current_branch(): ...
def get_latest_commit_message(): ...
def tag_exists(tag_name): ...
def remove_history_before_tag(tag_name) -> None: ...
def main() -> None: ...

from _typeshed import Incomplete
from ok.util.Util import delete_if_exists as delete_if_exists, get_logger as get_logger

logger: Incomplete

def delete_files(blacklist_patterns=..., whitelist_patterns=['adb.exe', 't64.exe', 'w64.exe', 'cli-64.exe', 'cli.exe', 'python*.exe', '*pip*'], root_dir: str = 'python') -> None: ...
def find_line_in_requirements(file_path, search_term, encodings=['utf-8', 'utf-16', 'ISO-8859-1', 'cp1252']): ...
def get_base_python_exe(): ...
def copy_python_files(python_dir, destination_dir) -> None: ...
def modify_venv_cfg(env_dir) -> None: ...
def get_env_path(name, dir: Incomplete | None = None): ...
def create_venv(name, dir: Incomplete | None = None): ...
def kill_exe(relative_path) -> None: ...

import math
import cv2
import numpy as np
import base64
import ctypes
import hashlib
import heapq
import importlib
import json
import logging
import os
import queue
import random
import subprocess
import threading
import traceback
from collections import defaultdict
from ctypes import wintypes
from dataclasses import dataclass, field
from functools import cmp_to_key
from logging.handlers import (
	TimedRotatingFileHandler,
	QueueHandler,
	QueueListener
)
from typing import List, Optional
from typing import Union, Dict

def init_class_by_name(module_name, class_name, *args, **kwargs):
  ...

class ExitEvent(threading.Event):

  def bind_queue(self, queue):
    ...

  def bind_stop(self, to_stop):
    ...

  def set(self):
    ...

class ScheduledTask:

  ...

class Handler:

  def __init__(self, event: ExitEvent, name=None):
    ...

  def _process_tasks(self):
    ...

  def post(self, task, delay=0, remove_existing=False, skip_if_running=False):
    ...

  def stop(self):
    ...

def write_json_file(file_path, data):
  ...

def is_admin():
  ...

def get_first_item(lst, default=None):
  ...

def safe_get(lst, idx, default=None):
  ...

def find_index_in_list(my_list, target_string, default_index=-1):
  ...

import sys
import time
import re
import shutil

def get_path_relative_to_exe(*files):
  ...

def get_relative_path(*files):
  ...

def install_path_isascii():
  ...

def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  ...

def ensure_dir_for_file(file_path):
  ...

def ensure_dir(directory, clear=False):
  ...

def delete_if_exists(file_path):
  ...

def delete_folders_starts_with(path, starts_with):
  ...

def handle_remove_error(func, path, exc_info):
  ...

def sanitize_filename(filename):
  ...

def clear_folder(folder_path):
  ...

def find_first_existing_file(filenames, directory):
  ...

def get_path_in_package(base, file):
  ...

def dir_checksum(directory, excludes=None):
  ...

def find_folder_with_file(root_folder, target_file):
  ...

def get_folder_size(folder_path):
  ...

import threading

def run_in_new_thread(func):
  ...

def check_mutex():
  ...

def all_pids() -> list[int]:
  ...

class UNICODE_STRING(ctypes.Structure):

  def create(cls, init_with: Union[str, int]):
    ...

  def __str__(self):
    ...

class SYSTEM_PROCESS_ID_INFORMATION(ctypes.Structure):

  ...

def ratio_text_to_number(supported_ratio):
  ...

def data_to_base64(data) -> str:
  """
    Serialize a dictionary or a list of dictionaries to a base64 encoded string.

    Args:
        data (Union[Dict, List[Dict]]): The data to serialize.

    Returns:
        str: The base64 encoded string.
    """
  ...

def base64_to_data(base64_str: str) -> Union[Dict, List[Dict]]:
  """
    Deserialize a base64 encoded string back to a dictionary or a list of dictionaries.

    Args:
        base64_str (str): The base64 encoded string.

    Returns:
        Union[Dict, List[Dict]]: The deserialized data.
    """
  ...

def get_readable_file_size(file_path):
  """Calculates the readable size of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The readable file size (e.g., "1.23 MB").
    """
  ...

def bytes_to_readable_size(size_bytes):
  """Converts bytes to a human-readable size.

    Args:
        size_bytes (int): The size in bytes.

    Returns:
        str: The human-readable size.
    """
  ...

def execute(game_path: str):
  ...

class Box:

  ...

def __repr__(self):
  ...

def __str__(self):
  ...

def scale(self, width_ratio: float, height_ratio: float):
  ...

def closest_distance(self, other: Box):
  ...

def relative_with_variance(self, relative_x: float = 0.5, relative_y: float = 0.5):
  ...

def crop_frame(self, frame):
  ...

def center(self):
  ...

def box_intersect(box1: Box, box2: Box) -> bool:
  ...

def compare_boxes(box1: Box, box2: Box) -> int:
  ...

def find_highest_confidence_box(boxes):
  ...

def sort_boxes(boxes: List[Box]):
  ...

def find_box_by_name(boxes: List[Box], names: object) -> Box:
  ...

def get_bounding_box(boxes: List[Box]):
  ...

def find_boxes_within_boundary(boxes: List[Box], boundary_box: Box, sort: bool = True) -> List[Box]:
  ...

def average_width(boxes: List[Box]):
  ...

def crop_image(image: object, box: Box = None) -> object:
  ...

def relative_box(frame_width, frame_height, x, y, to_x=1, to_y=1, width=0, height=0, name=None):
  ...

def find_boxes_by_name(boxes, names) -> list[Box]:
  ...

def is_close_to_pure_color(image: object, max_colors: int = 5000, percent: float = 0.97):
  ...

def get_mask_in_color_range(image: object, color_range: dict):
  ...

def get_connected_area_by_color(image: object, color_range: dict, connectivity: int = 4, gray_range: int = 0) -> tuple:
  ...

def color_range_to_bound(color_range: dict) -> tuple:
  ...

def calculate_colorfulness(image: object, box: Box = None) -> float:
  ...

def get_saturation(image: object, box: Box = None) -> float:
  ...

def find_color_rectangles(image: object,
  color_range: dict,
  min_width: int,
  min_height: int,
  max_width: int = -1,
  max_height: int = -1,
  threshold: float = 0.95,
  box: Box = None) -> list:
  ...

def is_pure_black(frame: object) -> bool:
  ...

def calculate_color_percentage(image: object, color_ranges: dict, box: Box = None) -> float:
  ...

def rgb_to_gray(rgb: object) -> float:
  ...

class CommunicateHandler(logging.Handler):

  def __init__(self):
    ...

  def emit(self, record):
    ...

def log_exception_handler(exc_type, exc_value, exc_traceback):
  ...

def config_logger(config=None, name='ok-script'):
  ...

class Logger:

  def __init__(self, name: str):
    ...

  def debug(self, message: str):
    ...

  def info(self, message: str):
    ...

  def warning(self, message: str):
    ...

  def error(self, message: str, exception: Optional[Exception] = None):
    ...

  def critical(self, message: str):
    ...

def exception_to_str(exception: Optional[Exception]) -> str:
  ...

def get_logger(name: str) -> Logger:
  ...

