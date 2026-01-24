import xlsxwriter as xlsx
import os
import numpy as np
from typing import Optional

DIRECTORY = 'XLSX Workbooks'

def ensure_directory(directory: str = DIRECTORY):
    """Ensures the export directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def _write_sheet(filename: str, headers: list[str], data_cols: list[np.ndarray | list]) -> None:
    """Helper function to write data to an Excel sheet."""
    ensure_directory()
    filepath = os.path.join(DIRECTORY, filename)
    
    workbook = xlsx.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    
    # Format
    cell_format = workbook.add_format()
    cell_format.set_bold(True)
    cell_format.set_align('center')
    cell_format.set_valign('vcenter')
    cell_format.set_font_size(12)
    cell_format.set_font_color('red')
    
    # Write Headers
    for col_idx, header in enumerate(headers):
        worksheet.set_column(col_idx, col_idx, 20) # Set reasonable width
        worksheet.write(0, col_idx, header, cell_format)
    
    # Write Data
    for col_idx, data in enumerate(data_cols):
        for row_idx, value in enumerate(data):
            worksheet.write(row_idx + 1, col_idx, value)
            
    workbook.close()

def export_cl_vs_velocity(cl: np.ndarray, v: np.ndarray) -> None:
    """Exports Lift Coefficient vs Velocity data."""
    _write_sheet('cl-vs-velocity.xlsx', ['CL', 'VELOCITY'], [cl, v])

def export_thrust_req_vs_velocity(thrust_req: np.ndarray, v: np.ndarray) -> None:
    """Exports Thrust Required vs Velocity data."""
    _write_sheet('thrust-vs-velocity.xlsx', ['THRUST REQUIRED (N)', 'VELOCITY (m/s)'], [thrust_req, v])

def export_power_vs_velocity(power_req: np.ndarray, v: np.ndarray) -> None:
    """Exports Power Required vs Velocity data."""
    _write_sheet('power-vs-velocity.xlsx', ['POWER REQUIRED (W)', 'VELOCITY (m/s)'], [power_req, v])

def export_drag_vs_velocity(drag: np.ndarray, v: np.ndarray) -> None:
    """Exports Drag vs Velocity data."""
    _write_sheet('drag-vs-velocity.xlsx', ['DRAG FORCE (N)', 'VELOCITY (m/s)'], [drag, v])

def export_lift2drag_vs_velocity(ltod: np.ndarray, v: np.ndarray) -> None:
    """Exports Lift-to-Drag Ratio vs Velocity data."""
    _write_sheet('ltod-vs-velocity.xlsx', ['LIFT-TO-DRAG RATIO', 'VELOCITY (m/s)'], [ltod, v])
