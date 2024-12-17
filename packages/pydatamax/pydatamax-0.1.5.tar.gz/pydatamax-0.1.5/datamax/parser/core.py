import os
import importlib


class ParserFactory:
    @staticmethod
    def create_parser(file_path: str, use_ocr: bool = False, use_gpu: bool = False, gpu_id: int = 6,
                      to_markdown: bool = False):
        """
        Create a parser instance based on the file extension.

        :param file_path: The path to the file to be parsed.
        :param use_ocr: Flag to indicate whether OCR should be used.
        :param use_gpu: Flag to indicate whether GPU should be used.
        :param gpu_id: The ID of the GPU to use.
        :param to_markdown: Flag to indicate whether the output should be in Markdown format.
                    (only supported files in .doc or .docx format)
        :return: An instance of the parser class corresponding to the file extension.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        parser_class_name = {
            '.docx': 'DocxParser',
            '.doc': 'DocParser',
            '.epub': 'EpubParser',
            '.html': 'HtmlParser',
            '.txt': 'TxtParser',
            '.pptx': 'PPtxParser',
            '.ppt': 'PPtParser',
            '.pdf': 'PdfParser',
            '.jpg': 'ImageParser',
            '.png': 'ImageParser'
        }.get(file_extension)

        if not parser_class_name:
            return None

        if file_extension == '.jpg' or file_extension == '.png':
            module_name = f'datamax.parser.image_parser'
        else:
            # Dynamically determine the module name based on the file extension
            module_name = f'datamax.parser.{file_extension[1:]}_parser'

        try:
            # Dynamically import the module and get the class
            module = importlib.import_module(module_name)
            parser_class = getattr(module, parser_class_name)

            # Special handling for PdfParser arguments
            if parser_class_name == 'PdfParser':
                return parser_class(file_path, use_ocr, use_gpu, gpu_id)
            elif parser_class_name == 'DocxParser' or parser_class_name == 'DocParser':
                return parser_class(file_path, to_markdown)
            else:
                return parser_class(file_path)

        except (ImportError, AttributeError) as e:
            raise e


class DataMaxParser:
    def __init__(self, file_path, use_ocr: bool = False, use_gpu: bool = False, gpu_id: int = 6,
                 to_markdown: bool = False):
        """
        Initialize the DataMaxParser with file path and parsing options.

        :param file_path: The path to the file or directory to be parsed.
        :param use_ocr: Flag to indicate whether OCR should be used.
        :param use_gpu: Flag to indicate whether GPU should be used.
        :param gpu_id: The ID of the GPU to use.
        :param to_markdown: Flag to indicate whether the output should be in Markdown format.
        """
        self.file_path = file_path
        self.use_ocr = use_ocr
        self.use_gpu = use_gpu
        self.gpu_id = gpu_id
        self.to_markdown = to_markdown

    def get_data(self):
        """
        Parse the file or directory specified in the file path and return the data.

        :return: A list of parsed data if the file path is a directory, otherwise a single parsed data.
        """
        try:
            if isinstance(self.file_path, list):
                data = [self._parse_file(f) for f in self.file_path]
                return data

            elif isinstance(self.file_path, str) and os.path.isfile(self.file_path):
                return self._parse_file(self.file_path)

            elif isinstance(self.file_path, str) and os.path.isdir(self.file_path):
                file_list = [os.path.join(self.file_path, file) for file in os.listdir(self.file_path)]
                data = [self._parse_file(f) for f in file_list if os.path.isfile(f)]
                return data
        except Exception as e:
            raise e

    def _parse_file(self, file_path):
        """
        Create a parser instance using ParserFactory and parse the file.

        :param file_path: The path to the file to be parsed.
        :return: The parsed data.
        """
        parser = ParserFactory.create_parser(file_path, self.use_ocr, self.use_gpu, self.gpu_id, self.to_markdown)
        if parser:
            return parser.parse(file_path)


if __name__ == '__main__':
    data = DataMaxParser(file_path=r"C:\Users\cykro\Desktop\数据工厂.pdf", use_ocr=True)
    data = data.get_data()
    print(data)