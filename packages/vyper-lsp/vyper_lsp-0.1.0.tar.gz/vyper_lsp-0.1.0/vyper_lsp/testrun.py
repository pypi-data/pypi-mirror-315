#!/usr/bin/env python3

from pathlib import Path
from vyper.ast.nodes import ImportFrom, Import
from vyper.cli.vyper_compile import get_search_paths
from vyper.compiler import CompilerData, FileInput, InputBundle
import os

from vyper.compiler.phases import FilesystemInputBundle
from vyper.semantics.types.user import EventT, FlagT

src = open("../examples/BondingCurveUser.vy").read()
path = Path("../examples/BondingCurveUser.vy")

file_input = FileInput(0, path, path, src)
search_paths = get_search_paths([str(path.parent)])
input_bundle = FilesystemInputBundle(search_paths)

compiler_data = CompilerData(file_input, input_bundle)

docstring = compiler_data.natspec

import_info = compiler_data.annotated_vyper_module.get_children(Import)[0]._metadata["import_info"]

module_metadata = compiler_data.annotated_vyper_module._metadata["type"]
