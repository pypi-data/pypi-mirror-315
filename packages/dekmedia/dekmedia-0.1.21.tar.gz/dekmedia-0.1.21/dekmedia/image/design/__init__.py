import os
import re
import numpy
from PIL import Image
from dektools.yaml import yaml
from dektools.file import read_file, FileHitChecker, sure_dir
from dektools.module import get_module_attr
from ...font.const import font_extensions
from ..const import image_extensions
from ..psd import PsdCanvas
from ..svg.load import load_svg
from ..svg.design import Manager as SvgManager


class Node:
    def __init__(self, manager: 'Manager', content):
        self.manager = manager
        self.content = content

    def make(self, args, params, attrs):
        raise NotImplementedError()


class SvgNode(Node):
    def make(self, args, params, attrs):
        return load_svg(self.content, attrs.get('width'), attrs.get('height'), fonts=self.manager.fonts_for_svg_loader)


class ImageNode(Node):
    def make(self, args, params, attrs):
        return self.content


class PsdNode(Node):
    def make(self, args, params, attrs):
        self.content.update(attrs)
        return self.content.render()


class SvgManagerNode(Node):
    def make(self, args, params, attrs):
        if args:
            width, height = args
        else:
            width, height = self.manager.svg_manager.parse_args(None)
        content = self.manager.svg_manager.make_svg(self.content, attrs)
        return load_svg(content.encode('utf-8'), width, height, fonts=self.manager.fonts_for_svg_loader)


class FunctionNode(Node):
    node_marker = '<<'
    re_var = r'\$\$([0-9a-zA-Z_]+)[\^]?'

    def __init__(self, manager, name, args, params, body):
        super().__init__(manager, body)
        self.name = name
        self.args = args
        self.params = params

    def trans_var(self, s, params):
        if s.startswith(self.node_marker):
            return self.manager.make_image(s[len(self.node_marker):])
        return yaml.loads(re.sub(self.re_var, lambda x: str(params[x.group(1)]), s))

    def _translate_list(self, params, data):
        result = []
        for item in data:
            if isinstance(item, str):
                item = self.trans_var(item, params)
            result.append(item)
        return result

    def _translate_map(self, params, data):
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                v = self.trans_var(v, params)
            if v is not None:
                result[k] = v
        return result

    def make(self, args, params, attrs):
        params = {**self.params, **params}
        image = None
        for index, (name, value) in enumerate(self.content.items()):
            value = value or {}
            if index == 0:
                node = self.manager.get_node(name)
                image = node.make(self._translate_list(params, self.args), params, self._translate_map(params, value))
            else:
                name = name.rstrip('+')
                args = value.pop('$', None) or []
                func = None
                ms = ('skimage', 'numpy', ('PIL.ImageOps', False))
                is_na = True
                for m in ms:
                    if not isinstance(m, str):
                        m, is_na = m
                    try:
                        func = get_module_attr(f'{m}.{name}')
                        break
                    except (ModuleNotFoundError, AttributeError):
                        pass
                if func is None:
                    raise AttributeError(f"Can't find func: {name}")
                if is_na:
                    if isinstance(image, Image.Image):
                        image = numpy.array(image)
                else:
                    if not isinstance(image, Image.Image):
                        image = Image.fromarray(image)
                image = func(image, *self._translate_list(params, args), **value)

        if not isinstance(image, Image.Image):
            return Image.fromarray(image)
        return image


class Manager:
    ignore_file = '.designignore'
    entry_marker = '>>'
    function_node_cls = FunctionNode
    svg_node_cls = SvgNode
    image_node_cls = ImageNode
    psd_node_cls = PsdNode
    svg_manager_node_cls = SvgManagerNode
    svg_manager_cls = SvgManager

    def __init__(self):
        self.svg_manager = self.svg_manager_cls()
        self.entry_names = []
        self.function_map = {}
        self.svg_map = {}
        self.font_map = {}
        self.image_map = {}
        self.psd_map = {}

    def dump(self, path, args=None, params=None, attrs=None):
        sure_dir(path)
        for name, image in self.entries(args, params, attrs):
            image.save(os.path.join(path, name + '.png'))

    def entries(self, args=None, params=None, attrs=None):
        for name in self.entry_names:
            yield name, self.make_image(name, args, params, attrs)

    def make_image(self, name, args=None, params=None, attrs=None):
        return self.get_node(name).make(args, params or {}, attrs or {})

    def get_node(self, name):
        return self.function_map.get(name) or \
            self.new_svg_node(name) or \
            self.new_image_node(name) or \
            self.new_psd_node(name) or \
            self.new_svg_manager_node(name)  # always at end

    def new_svg_node(self, name):
        path = self.svg_map.get(name)
        if path:
            return self.svg_node_cls(self, read_file(path))

    def new_image_node(self, name):
        path = self.image_map.get(name)
        if path:
            return self.image_node_cls(self, Image.open(path))

    def new_psd_node(self, name):
        path = self.psd_map.get(name)
        if path:
            return self.psd_node_cls(self, PsdCanvas.load(path))

    def new_svg_manager_node(self, name):
        return self.svg_manager_node_cls(self, name)

    @property
    def all_font_map(self):
        return {**self.svg_manager.font_map, **self.font_map}

    @property
    def fonts_for_svg_loader(self):
        return {k: {'font_path': v} for k, v in self.all_font_map.items()}

    def load_file_yaml(self, path):
        data_map = yaml.load(path)
        for name, body in data_map.items():
            args = body.pop('$', None) or []
            params = body.pop('$$', None) or {}
            if name.endswith(self.entry_marker):
                name = name[:len(name) - len(self.entry_marker)]
                self.entry_names.append(name)
            self.function_map[name] = self.function_node_cls(self, name, args, params, body)

    def load_file_svg(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.svg_map[name] = path

    def load_file_psd(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.psd_map[name] = path

    def load_file_font(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.font_map[name] = path

    def load_file_image(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.image_map[name] = path

    def load_path(self, *paths):
        def walk(fp, match, _):
            if match:
                return
            ext = os.path.splitext(fp)[-1].lower()
            if ext == '.svg':
                self.load_file_svg(fp)
            elif ext == '.yaml':
                self.load_file_yaml(fp)
            elif ext == '.psd':
                self.load_file_psd(fp)
            elif ext in font_extensions:
                self.load_file_font(fp)
            elif ext in image_extensions:
                self.load_file_image(fp)

        for path in paths:
            self.svg_manager.load_path(path)
            FileHitChecker(path, self.ignore_file).walk(walk)
