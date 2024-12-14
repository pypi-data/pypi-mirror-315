from pathlib import Path


_ERROR_MSG =\
	"The path must be of type str or pathlib.Path. None is not allowed."
_ERROR_MSG_NONE =\
	"The path must be None or of type str or pathlib.Path."


def _raise_type_error(is_none_allowed):
	message = _ERROR_MSG_NONE if is_none_allowed else _ERROR_MSG
	raise TypeError(message)


def ensure_path_is_pathlib(some_path, is_none_allowed):
	"""
	If argument some_path is a string, this function converts it to a
	pathlib.Path instance, which it returns. If some_path is a pathlib.Path
	instance, this function returns some_path.

	If argument some_path is None and argument is_none_allowed is True, this
	function returns None. However, if is_none_allowed is False, a TypeError is
	raised.

	If argument some_path is not None nor an instance of str or pathlib.Path,
	a TypeError is raised.

	Parameters:
		some_path (str or pathlib.Path): the path to a file or directory.
		is_none_allowed (bool): determines whether some_path can be None.

	Returns:
		pathlib.Path: the path to a file or directory, possibly None.

	Raises:
		TypeError: if some_path is of a wrong type.
	"""
	if isinstance(some_path, Path) or is_none_allowed and some_path is None:
		return some_path
	elif isinstance(some_path, str):
		return Path(some_path)
	else:
		_raise_type_error(is_none_allowed)


def ensure_path_is_str(some_path, is_none_allowed):
	"""
	If argument some_path is a pathlib.Path instance, this function converts
	it to a string, which it returns. If some_path is a string, this function
	returns some_path.

	If argument some_path is None and argument is_none_allowed is True, this
	function returns None. However, if is_none_allowed is False, a TypeError is
	raised.

	If argument some_path is not None nor an instance of str or pathlib.Path,
	a TypeError is raised.

	Parameters:
		some_path (str or pathlib.Path): the path to a file or directory.
		is_none_allowed (bool): determines whether some_path can be None.

	Returns:
		str: the path to a file or directory, possibly None.

	Raises:
		TypeError: if some_path is of a wrong type.
	"""
	if isinstance(some_path, str) or is_none_allowed and some_path is None:
		return some_path
	elif isinstance(some_path, Path):
		return str(some_path)
	else:
		_raise_type_error(is_none_allowed)
