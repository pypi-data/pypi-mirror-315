from typing import *  # type: ignore

import imy.docstrings


def _documented_function_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return set(docs.functions)


def _documented_attribute_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return set(docs.attributes)


class Parent:
    """
    # Leading Headings 1 are stripped

    This is the summary.

    This is the details. They can be very long and span multiple lines. They can
    even contain multiple paragraphs.

    Just like this one.

    ## Heading 2

    Any non-key sections are also part of the details.

    This is the end of the details.

    ## Attributes

    int_attribute: <int>

    `float_attribute`: <float>

    str_attribute: <str>

    ## Metadata

    public: False
    """

    int_attribute: int
    float_attribute: float
    str_attribute: str

    @property
    def bytes_property(self) -> bytes:
        """
        This is the getter function of `bytes_property`
        """
        return b""

    @bytes_property.setter
    def bytes_property(self, value: str | bytes) -> None:
        """
        This is the setter function of `bytes_property`
        """
        _ = value

    def numeric_function(self, x: int) -> float:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <int>

        ## Raises

        `ValueError`: <raise-value-error>
        """
        return float(x)

    def overridden_function(self) -> float:
        """
        docstring for `overridden_function`
        """
        return 1.5


class Child(Parent):
    """
    Children are parents too!

    ## Attributes

    bool_attribute: <bool>

    ## Metadata

    public: True

    experimental: True
    """

    bool_attribute: bool

    async def list_function(self, x: str) -> list:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <str>
        """
        return [x]

    def overridden_function(self) -> int:
        return 1


def test_parse_class_docstring() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Parent)

    assert docs.name == "Parent"
    assert docs.summary == "This is the summary."

    assert docs.details is not None
    assert docs.details.startswith("This is the details.")
    assert docs.details.endswith("This is the end of the details.")

    assert _documented_function_names(docs) == {
        "numeric_function",
        "overridden_function",
    }

    numeric_function_docs = docs.functions["numeric_function"]
    assert numeric_function_docs.owner is docs
    assert numeric_function_docs.name == "numeric_function"
    assert numeric_function_docs.synchronous is True
    assert numeric_function_docs.return_type is float
    assert numeric_function_docs.summary == "<function summary>"
    assert numeric_function_docs.details == "<function details>"

    assert len(numeric_function_docs.parameters) == 2
    param1, param2 = numeric_function_docs.parameters.values()

    assert param1.owner is numeric_function_docs
    assert param1.name == "self"

    assert param2.owner is numeric_function_docs
    assert param2.name == "x"
    assert param2.type is int
    assert param2.description == "<int>"

    overridden_function_docs = docs.functions["overridden_function"]
    assert overridden_function_docs.owner is docs
    assert overridden_function_docs.name == "overridden_function"
    assert overridden_function_docs.synchronous is True
    assert overridden_function_docs.return_type is float
    assert overridden_function_docs.summary == "docstring for `overridden_function`"
    assert overridden_function_docs.details is None

    assert len(numeric_function_docs.raises) == 1
    assert numeric_function_docs.raises[0] == (
        "ValueError",
        "<raise-value-error>",
    )

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
    }

    for attr in docs.attributes.values():
        assert attr.owner is docs
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    for prop in docs.properties.values():
        assert prop.owner is docs

        assert prop.getter.owner is prop

        assert prop.setter is not None
        assert prop.setter.owner is prop

    assert docs.metadata.public is False
    assert docs.metadata.experimental is False


def test_parse_class_docstring_with_inheritance() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Child)

    print(docs)

    assert docs.name == "Child"
    assert docs.summary == "Children are parents too!"
    assert docs.details is None

    assert _documented_function_names(docs) == {
        "numeric_function",
        "list_function",
        "overridden_function",
    }

    for func in docs.functions.values():
        assert func.owner is docs

        if func.name == "numeric_function":
            assert func.synchronous is True
            assert func.return_type is float
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            param1, param2 = func.parameters.values()

            assert param1.name == "self"

            assert param2.name == "x"
            assert param2.type is int
            assert param2.description == "<int>"

            assert len(func.raises) == 1
            assert func.raises[0] == ("ValueError", "<raise-value-error>")

        elif func.name == "list_function":
            assert func.synchronous is False
            assert func.return_type is list
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            param1, param2 = func.parameters.values()

            assert param1.name == "self"

            assert param2.name == "x"
            assert param2.type is str
            assert param2.description == "<str>"

            assert len(func.raises) == 0

        elif func.name == "overridden_function":
            assert func.owner is docs
            assert func.synchronous is True
            assert func.return_type is int
            assert func.summary == "docstring for `overridden_function`"
            assert func.details is None

        else:
            assert False, f"Unexpected function: {func.name}"

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
        "bool_attribute",
    }

    for attr in docs.attributes.values():
        assert attr.owner is docs
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    assert docs.metadata.public is True
    assert docs.metadata.experimental is True
