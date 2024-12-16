from ctypes import *
import argparse
from errors import * 

lib = cdll.LoadLibrary("./vendor/liboasyamlcombine.so")

def resolve_references(input_path: str, output_path: str, refs_dir: str, inline_local: bool, inline_remote: bool, keep_local: bool):
	result = lib.oasYamlCombine(
		c_char_p(str.encode(input_path)),
		c_char_p(str.encode(output_path)),
		c_char_p(str.encode(refs_dir)),
		1 if inline_local else 0,
		1 if inline_remote else 0,
		1 if keep_local else 0
	)

	if result == 0:
		return
	
	raise {
        11: InputFilepathErr,
        12: InputStdinErr,
        13: InputRefDirCwdErr,
        21: OutputFilepathErr,
        22: OutputFilepathErr,
		23: OutputStdoutErr,
        31: RootDocumentErr,
        32: RefResolveErr,
    }.get(result, UnexpectedErr)


if __name__ == '__main__':
	parser=argparse.ArgumentParser()

	parser.add_argument("--input", help="path to the input yaml file to be processed. Providing --input sets the ref directory to the parent directory of provided input path. When not provided, stdin is used to read the file contents", default="")
	parser.add_argument("--output", help="path to the output yaml file. When not provided stdout is used to return the result of documents combining", default="")
	parser.add_argument("--refsdir", help="directory used as a root for ref relative paths resolution. By default current working directory is used, unless the input is provided", default="")
	parser.add_argument("--inlinelocal", help="should local refs be inlined in place when resolved. When set to False, local references are left in place since they are skipped from resolving. False by default", action="store_true", default=False)
	parser.add_argument("--inlineremote", help="should remote refs be inlined in place rather than being placed in a local equivalent. False by default. Note: remote refs are always resolved and never left in place when encountered in a document, since it's the whole point of combining documents", action="store_true", default=False)
	parser.add_argument("--keeplocal", help="keep local refs after inlining. Makes sense only when --inlinelocal is specified as true, otherwise has no effect in order to prevent outputting incorrect yaml file with missing references", action="store_true", default=False)

	args=parser.parse_args()

	resolve_references(input_path=args.input, output_path=args.output, refs_dir=args.refsdir, inline_local=args.inlinelocal, inline_remote=args.inlineremote, keep_local=args.keeplocal)