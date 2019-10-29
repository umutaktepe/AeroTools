import xlsxwriter as xlsx
import os

directory = 'XLSX Workbooks'


class Export:

    def __init__(self):

        super(Export, self).__init__()

    def clvsVelocity(self, cl, v):

        try:
            os.mkdir(directory)
        except OSError:
            pass

        cl_data = xlsx.Workbook('XLSX Workbooks/cl-vs-velocity.xlsx')

        cell_format = cl_data.add_format()
        cell_format.set_bold(True)
        cell_format.set_align('center')
        cell_format.set_valign('vcenter')
        cell_format.set_font_size('12')
        cell_format.set_font_color('red')

        cl_worksheet = cl_data.add_worksheet()
        cl_worksheet.set_column('A:B', 15)
        cl_worksheet.write(0, 0, 'CL', cell_format)
        cl_worksheet.write(0, 1, 'VELOCITY', cell_format)

        row = 1
        row_v = 1

        for i in cl:
            cl_worksheet.write(row, 0, i)
            row += 1

        for j in v:
            cl_worksheet.write(row_v, 1, j)
            row_v += 1

        return cl_data.close()

    def thrReqvsVelocity(self, thrReq, v):

        try:
            os.mkdir(directory)
        except OSError:
            pass

        tr_data = xlsx.Workbook('XLSX Workbooks/thrust-vs-velocity.xlsx')

        cell_format = tr_data.add_format()
        cell_format.set_bold(True)
        cell_format.set_align('center')
        cell_format.set_valign('vcenter')
        cell_format.set_font_size('12')
        cell_format.set_font_color('red')

        tr_worksheet = tr_data.add_worksheet()
        tr_worksheet.set_column('A:B', 22)
        tr_worksheet.write(0, 0, 'THRUST REQUIRED (N)', cell_format)
        tr_worksheet.write(0, 1, 'VELOCITY (m/s)', cell_format)

        row = 1
        row_v = 1

        for i in thrReq:
            tr_worksheet.write(row, 0, i)
            row += 1

        for j in v:
            tr_worksheet.write(row_v, 1, j)
            row_v += 1

        return tr_data.close()

    def powervsVelocity(self, powReq, v):

        try:
            os.mkdir(directory)
        except OSError:
            pass

        pow_data = xlsx.Workbook('XLSX Workbooks/power-vs-velocity.xlsx')

        cell_format = pow_data.add_format()
        cell_format.set_bold(True)
        cell_format.set_align('center')
        cell_format.set_valign('vcenter')
        cell_format.set_font_size('12')
        cell_format.set_font_color('red')

        pow_worksheet = pow_data.add_worksheet()
        pow_worksheet.set_column('A:B', 22)
        pow_worksheet.write(0, 0, 'POWER REQUIRED (W)', cell_format)
        pow_worksheet.write(0, 1, 'VELOCITY (m/s)', cell_format)

        row = 1
        row_v = 1

        for i in powReq:
            pow_worksheet.write(row, 0, i)
            row += 1

        for j in v:
            pow_worksheet.write(row_v, 1, j)
            row_v += 1

        return pow_data.close()

    def dragvsVelocity(self, drag, v):

        try:
            os.mkdir(directory)
        except OSError:
            pass

        drag_data = xlsx.Workbook('XLSX Workbooks/drag-vs-velocity.xlsx')

        cell_format = drag_data.add_format()
        cell_format.set_bold(True)
        cell_format.set_align('center')
        cell_format.set_valign('vcenter')
        cell_format.set_font_size('12')
        cell_format.set_font_color('red')

        drag_worksheet = drag_data.add_worksheet()
        drag_worksheet.set_column('A:B', 20)
        drag_worksheet.write(0, 0, 'DRAG FORCE (N)', cell_format)
        drag_worksheet.write(0, 1, 'VELOCITY (m/s)', cell_format)

        row = 1
        row_v = 1

        for i in drag:
            drag_worksheet.write(row, 0, i)
            row += 1

        for j in v:
            drag_worksheet.write(row_v, 1, j)
            row_v += 1

        return drag_data.close()

    def lift2dragvsVelocity(self, ltod, v):

        try:
            os.mkdir(directory)
        except OSError:
            pass

        ltod_data = xlsx.Workbook('XLSX Workbooks/ltod-vs-velocity.xlsx')

        cell_format = ltod_data.add_format()
        cell_format.set_bold(True)
        cell_format.set_align('center')
        cell_format.set_valign('vcenter')
        cell_format.set_font_size('12')
        cell_format.set_font_color('red')

        ltod_worksheet = ltod_data.add_worksheet()
        ltod_worksheet.set_column('A:B', 24)
        ltod_worksheet.write(0, 0, 'LIFT-TO-DRAG RATIO', cell_format)
        ltod_worksheet.write(0, 1, 'VELOCITY (m/s)', cell_format)

        row = 1
        row_v = 1

        for i in ltod:
            ltod_worksheet.write(row, 0, i)
            row += 1

        for j in v:
            ltod_worksheet.write(row_v, 1, j)
            row_v += 1

        return ltod_data.close()

