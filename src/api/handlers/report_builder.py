from fpdf import FPDF, HTMLMixin
from io import BytesIO
import pandas as pd
import dataframe_image as dfi
import matplotlib
import base64
import os
from icecream import ic
from enum import Enum

from mock.report_data_labels import MOCK_DATA_LABELS as mock_labels


class ReportConfig:
    document_width: int = 211
    document_height: int = 297
    header_image_path: str = "static/images/header.png"
    footer_image_path: str = "static/images/footer.png"
    default_line_break_spaces: int = 10

    class FontFamily(Enum):
        MAIN_FONT = 'Helvetica'

    class FontSize(Enum):
        TITLE_FONT_SIZE = 20
        SUBTITLE_FONT_SIZE = 14
        GENERAL_TEXT_FONT_SIZE = 12
        FOOTER_OR_LEGEND = 8
    
    class FontStyles(Enum):
        TITLE = "b"
        SUBTITLE = "b"
        HEADER_TEXT = "b"
        CELL_TEXT = ""
        TEXT = ""
        FOOTER_OR_LEGEND = "I"

    class Colors(Enum):
        BLUE = {
            "r": 3,
            "g": 78,
            "b": 162
        }
        GRAY = {
            "r": 128,
            "g": 128,
            "b": 128
        }
        BLACK = {
            "r": 0,
            "g": 0,
            "b": 0
        }

    @staticmethod
    def get_complete_font_style(font_style: FontStyles) -> dict:
        if font_style == ReportConfig.FontStyles.TITLE:
            size = ReportConfig.FontSize.TITLE_FONT_SIZE
        elif font_style == ReportConfig.FontStyles.SUBTITLE:
            size = ReportConfig.FontSize.SUBTITLE_FONT_SIZE
        elif font_style == ReportConfig.FontStyles.FOOTER_OR_LEGEND:
            size = ReportConfig.FontSize.FOOTER_OR_LEGEND
        else:
            size = ReportConfig.FontSize.GENERAL_TEXT_FONT_SIZE

        return {
            "family": ReportConfig.FontFamily.MAIN_FONT.value,
            "style": font_style.value,
            "size": size.value,
        }
    

class PDF(FPDF):
    def header(self):
        self.image("static/images/header.png", 0, 0, ReportConfig.document_width)
        self.set_y(43)

    def footer(self):
        self.set_y(-1)
        self.image("static/images/footer.png", 0, None, w=ReportConfig.document_width, h=3)
        self.set_y(-15)
        self.set_font(**ReportConfig.get_complete_font_style(ReportConfig.FontStyles.FOOTER_OR_LEGEND))
        self.set_text_color(128)
        self.cell(0, 10, 'Pagina ' + str(self.page_no()), 0, 0, 'C')


class ReportBuilder:
    def __init__ (self, report_data: dict) -> None:
        self.report_data = report_data
        self.pdf = PDF()

    def _write_content_text(self, text: str, font_style: ReportConfig.FontStyles, font_color: ReportConfig.Colors, line_break_spaces: int, has_line_break: bool = True) -> None:
        self.pdf.set_font(**ReportConfig.get_complete_font_style(font_style))
        self.pdf.set_text_color(**font_color.value)
        self.pdf.write(5, text)
        if has_line_break:
            self.pdf.ln(line_break_spaces)
    
    def _write_divisory_line(self) -> None:
        self.pdf.set_line_width(0.3)
        self.pdf.set_draw_color(**ReportConfig.Colors.BLUE.value)
        self.pdf.line(
            10,
            self.pdf.get_y(),
            200, 
            self.pdf.get_y()
            )
        self.pdf.set_draw_color(**ReportConfig.Colors.BLACK.value)
        self.pdf.ln(5)

    def _write_simple_table(self, dict_values: dict, dict_key: str) -> None:
        df = ReportBuilder._parse_data_to_table(dict_values)
        labels = mock_labels[dict_key]
        labels_keys = list(labels.keys())
        df = df[labels_keys]
        self.pdf.set_font(**ReportConfig.get_complete_font_style(ReportConfig.FontStyles.CELL_TEXT))
        self.pdf.set_text_color(**ReportConfig.Colors.BLACK.value)
        def get_row(value):
            if "," in value:
                return f"<td>{value.replace(',', '<br/>')}</td>"
            return f"<td>{value}</td>"
        list_of_rows = "".join(
                            [
                                f"""
                                <tr>
                                    <font color="black"><td>{labels[col]}</td></font>
                                    {get_row(str(df[col].values[0]))}
                                </tr>
                                """
                                for col in labels_keys
                            ]
                        )
        self.pdf.write_html(
            f"""
            <table border="1" cellpadding="2" cellspacing="0">
                <tbody>
                    {
                        list_of_rows
                    }
                </tbody>
            </table>""",
            table_line_separators=True,
        )
                
    
    @staticmethod
    def _parse_data_to_table(dict_data: dict) -> pd.DataFrame:
        """
        Parse data to a pandas DataFrame
        """
        return pd.DataFrame([dict_data])
    
    #   def save_table_as_image(styled_df):
    #       dfi.export(styled_df, 'temp/table.png', table_conversion='matplotlib', fontsize=7)
    #       return 'temp/table.png'

    #    def delete_temp_image():
    #        os.remove('temp/table.png')
    #
    #    def write_image_to_pdf(pdf, styled_df, width):
    #        image_path = save_table_as_image(styled_df)
    #        pdf.image(image_path)
    #        pdf.ln(10)
    #        delete_temp_image()
        
    def _create_report_title(self, title: str, subtitle: str, date: str) -> None:
        # Add main title
        self._write_content_text(
            title,
            ReportConfig.FontStyles.TITLE,
            ReportConfig.Colors.BLUE,
            ReportConfig.default_line_break_spaces
            )
        # Add subtitle
        self._write_content_text(
            subtitle,
            ReportConfig.FontStyles.SUBTITLE,
            ReportConfig.Colors.GRAY,
            ReportConfig.default_line_break_spaces
            )
        # Add date of report/%m/%Y")
        self._write_content_text(
            date,
            ReportConfig.FontStyles.TEXT,
            ReportConfig.Colors.GRAY,
            ReportConfig.default_line_break_spaces
            )
        # Add little break to keep the content organized
        self.pdf.ln(5)

    def _create_map_section(self, section_title: str, map_image_base64: str) -> None:
        self._write_content_text(
            section_title,
            ReportConfig.FontStyles.SUBTITLE,
            ReportConfig.Colors.BLUE,
            ReportConfig.default_line_break_spaces
        )
        self._write_divisory_line()
        # save base64 image to .png file
        ic("encoding...")
        img_data = map_image_base64.encode()
        ic("decoding...")
        img_content = base64.b64decode(img_data)
        ic("writing to bytes...")
        map_image = BytesIO(img_content)
        ic("plotting image...")
        # image centered in the page
        self.pdf.image(
            map_image,
            ReportConfig.document_width/3-10,
            self.pdf.get_y(),
            ReportConfig.document_width/3+25,
            ReportConfig.document_width/3+30
            )
        self.pdf.ln(ReportConfig.document_width/3+40)
        
    def _create_data_sections(self, data: dict) -> None:
        for key, value in data.items():
            self._write_content_text(
                f"{key}:",
                ReportConfig.FontStyles.SUBTITLE,
                ReportConfig.Colors.BLUE,
                ReportConfig.default_line_break_spaces
                )
            self._write_divisory_line()
            self._write_simple_table(value, key)
            self.pdf.ln(ReportConfig.default_line_break_spaces)

    def build_report(self):
        ic(f"Building report...")
        self.pdf.add_page()

        self._create_report_title(
            self.report_data["metadata"]["title"],
            self.report_data["metadata"]["subtitle"],
            self.report_data["metadata"]["date"]
            )
        
        try:
            self._create_map_section(
                "Mapa do Estado:",
                self.report_data["screenshot"]
                )
        except:
            ic("Map image unprocessable")
        
        self._create_data_sections(
            self.report_data["data"]
            )

        pdf_output = BytesIO()
        self.pdf.output(pdf_output, 'F')
        pdf_output.seek(0)

        return pdf_output