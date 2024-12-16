#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    py 的 xlwt 库是一个用于写入数据到旧式的 Excel 文件
    （即 `.xls` 格式，Excel 97-2003）的第三方库。

    它提供一系列功能，
    让用户可以通过 py 脚本创建和编辑 `.xls` 格式的电子表格文档。

    以下是一些 xlwt 库的主要功能：
        - 创建新的 Excel 文件：
          可以创建全新的 `.xls` 文件，并添加工作表。

        - 写入数据：能够将数据写入单元格中，包括文本、数字和公式。

        - 格式化内容：支持字体样式、单元格背景颜色、
          单元格边框等多种格式设置，
          使得输出文档具有更好的可读性和专业性。

        - 合并单元格：可以合并一系列的单元格，
          用于显示跨多个行或列的数据。

        - 日期和时间支持：允许在单元格中插入日期和时间对象，
          并按照特定格式显示它们。

        - 公式支持：能够插入 Excel 公式，自动计算相应值。

        - 调整行高列宽：为更好地展示内容，
          可以针对具体需求调整行高和列宽。

        - 添加批注：可以在单元格上添加用户批注。

        - 保护工作表：支持对工作表进行密码保护，
          防止未授权修改数据。

        - 写入超链接：允许向单元格添加超链接。

    需要注意的是，虽然 xlwt 在操作 `.xls` 文件时非常有用，
    但它不支持较新版本 Excel 使用的 `.xlsx` 格式。

    如果需要处理 `.xlsx` 文件，则应使用例如 openpyxl, xlsxwriter,
    或者 pandas with openpyxl/xlsxwriter as engine 这样的库。

    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import xlwt

DEFAULT_WIDTH = 35
# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性
# 如果定义了 `__all__`，只有在这个列表中的属性才会被导入
# 如果没有定义 `__all__`，那么默认导入模块中不以下划线开头的所有属性
__all__ = [
    "create_excel"
]

# 将当前运行的 py 文件所在的上两级目录加入到 py 的【系统路径】中
# 使得在这个【根目录】下的【模块】和【包】可以被当前文件所引用
current_file_path = Path(__file__).absolute()
# 移动到上两级目录以获取【根路径】
root_path = current_file_path.parent.parent
# 将【根路径】作为【系统路径】加入 `sys.path`
sys.path.append(str(root_path))


def __set_col_width(
        sheet: xlwt.Worksheet,
        col_idx: int,
        max_width: int) -> None:
    """
        设置特定列的宽度。

        该函数根据最大字符数调整 Excel 工作表中特定列的宽度。

        需要注意的是，这里使用的宽度单位是 xlwt 库特有的，
        其中大约 256 单位等于一个字符的宽度。

    :param sheet: 需要设置列宽的 xlwt.Worksheet 对象。
    :param col_idx: 需要设置宽度的列索引（从 0 开始）。
    :param max_width: 该列预期能容纳的最大字符数。
    :return: 无返回值。
    """
    # 假设一个字符的宽度大约为 256 单位（这是 xlwt 中的单位）
    # (256 是在 xlwt 库中用于定义单个标准 Excel 格子单位长度为 1 个字符宽度。
    # 因为 Excel 不使用像素或者点这样常见图形界面长度单位，
    # 而是用自己特定算法决定格子大小；
    # 这里乘以 256 就是将想要存进去文字大小转换成 Excel 格子大小单位。)
    # 可能需要根据实际使用的字体和字符调整乘数
    # 代码将指定列(col_idx)的宽度设置成 `max_width * 256`，
    # 即预期能容纳 `max_width` 这么多个字符
    sheet.col(col_idx).width = max_width * 256


def __create_style() -> xlwt.XFStyle:
    """
        创建并返回一个 `xlwt.XFStyle` 样式对象，
        用于 Excel 单元格格式设置。

        该样式包括：
            - 文本居中对齐

            - 单元格边框为细线

    :return: 配置了文本对齐和边框样式的 `xlwt.XFStyle` 对象。
    """
    # 创建一个新的 `XFStyle` 对象
    # 该对象用于定义 Excel 单元格的格式
    style = xlwt.XFStyle()
    # 创建一个 `Alignment` 对象
    # 负责设置单元格内文本的对齐方式
    alignment = xlwt.Alignment()
    # 设置水平对齐方式为居中
    # 这意味着单元格内的文本会水平居中显示
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    # 设置垂直对齐方式为居中
    # 这意味着单元格内的文本会垂直居中显示
    alignment.vert = xlwt.Alignment.VERT_CENTER
    # 将之前设置好的对齐方式应用到样式对象 `style` 上
    # 此时 `style` 已经具有文本居中对齐的功能
    style.alignment = alignment
    # 创建一个 `Borders` 对象，用于设置单元格边框样式
    borders = xlwt.Borders()
    # 设置上、下、左、右四个边框都为细线( THIN )
    # 这里使用链式赋值来简化代码，同时设置四个边界值
    borders.left \
        = borders.right \
        = borders.top \
        = borders.bottom \
        = xlwt.Borders.THIN
    # 将之前设置好的边框应用到样式对象 `style` 上
    # 此时样式对象已经具有【文本居中对齐】和【细线边框】两种功能
    style.borders = borders
    return style


def __add_rows(
        sheet: xlwt.Worksheet,
        rows: List[List],
        field_names: Optional[List[str]] = None,
        style: Optional[xlwt.XFStyle] = None,
        default_width: int = DEFAULT_WIDTH) -> Tuple[int, int]:
    """
        将数据行添加到 Excel 工作表中，并设置列宽。

        该函数首先根据提供的字段名（如果有）创建标题行（即表头，并非真的标题）。

        接着，将数据行写入工作表中，每个单元格可以应用指定的样式
        （主要是文字居中以及添加细边框线）。

        最后，函数会根据数据内容自动调整每一列的宽度。

    :param sheet: 要写入数据的工作表对象。
    :param rows: 需要写入工作表的二维数据列表。
    :param field_names:
    可选参数，表示标题行字段名列表，
    如果提供，则首先将这些字段名写入第一行。
    :param style: 可选参数，单元格样式对象，
    指定样式将应用于所有单元格，默认为 None。
    :param default_width:
    设置工作表中每一列宽度的默认值，
    默认情况下使用常量 DEFAULT_WIDTH。
    如果调用时提供了其他值，则使用该值覆盖默认宽度。
    宽度单位通常是字符数，
    具体数值取决于使用的字体和 Excel 版本。
    :return: 返回一个元组，
    包含实际添加到工作表的总行数和最大列数。
    """
    # 初始化记录当前写入的行号和最大列数
    row_num = 0
    max_col_num = 0
    # 如果存在字段名称列表，则先创建标题行
    if field_names:
        for col_num, field_name in enumerate(field_names):
            sheet.write(
                row_num,
                col_num,
                field_name,
                style if style else None
            )
            max_col_num = max(max_col_num, col_num + 1)
        # 数据行完成后，移动到下一行准备继续写入
        row_num += 1
    for row in rows:
        for col_num, cell_value in enumerate(row):
            sheet.write(
                row_num,
                col_num,
                cell_value,
                style if style else None
            )
            max_col_num = max(max_col_num, col_num + 1)
        row_num += 1
    # 调整每一列的宽度以适应其内容
    for col_idx in range(max_col_num):
        max_width = default_width
        for row in rows:
            # 检查所有已添加数据中对应列索引位置上最长内容长度
            # 并更新最大宽度
            if len(row) > col_idx:
                max_width = max(
                    max_width,
                    len(str(row[col_idx]))
                )
        __set_col_width(
            sheet=sheet,
            col_idx=col_idx,
            max_width=max_width
        )
    return row_num, max_col_num


def create_excel(
        filename: str,
        rows: List[List],
        field_names: Optional[List[str]] = None,
        default_width: int = DEFAULT_WIDTH,
        sheet_name: str = "Sheet1") -> None:
    """
        创建并保存一个 Excel 文件，
        包含指定的行数据和字段名称。

    :param filename:
    要创建的文件名，必须以 ".xls" 为扩展名。
    :param rows: 表格中要填写的数据，每个子列表代表一行。
    :param field_names:
    可选参数，用于指定表格的列标题，传入列表形式。
    如果提供，则该列表中的字符串将作为每列的标题。
    列标题数量应与 rows 中列表长度一致。
    :param default_width:
    设置工作表中每一列宽度的默认值，
    默认情况下使用常量 DEFAULT_WIDTH。
    如果调用时提供了其他值，则使用该值覆盖默认宽度。
    宽度单位通常是字符数，
    具体数值取决于使用的字体和 Excel 版本。
    :param sheet_name:
    Excel 文件中工作表的名称，默认为 "Sheet1"。
    :return: 无返回值。
    函数执行后将在指定路径下创建
    一个包含给定数据和设置的 Excel 文件。
    """
    if not filename.endswith(".xls"):
        raise ValueError(
            "文件名必须以 \".xls\" 结尾。"
        )
    if field_names is not None \
            and not isinstance(field_names, list):
        raise ValueError(
            "\"field_names\" 必须是个 \"list\"，如果提供的话。"
        )
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetname=sheet_name)
    __add_rows(
        sheet=ws,
        rows=rows,
        field_names=field_names,
        style=__create_style(),
        default_width=default_width
    )
    wb.save(filename_or_stream=filename)
