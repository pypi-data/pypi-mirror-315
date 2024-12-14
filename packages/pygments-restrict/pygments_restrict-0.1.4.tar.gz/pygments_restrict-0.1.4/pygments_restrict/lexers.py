from pygments.lexer import RegexLexer, bygroups
from pygments.token import (
    Comment,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    Text,
)

__all__ = ["ResourceFileLexer"]


class ResourceFileLexer(RegexLexer):
    name = "Restrict Framework Resource Language"
    aliases = ["restrict-resources", "restrict-resource"]
    filenames = ["*.resources", "*.resource"]
    mimetypes = ["text/x-restrict-resource"]

    def prop_callback(self, match):
        yield match.start(1), Name.Variable, match.group(1)
        further = [x for x in match.group(2).split(".") if x != ""]
        if len(further) > 0:
            start = match.start(2)
            for prop in further:
                yield start, Operator, "."
                start += 1
                yield start, Name.Property, prop
                start += len(prop)

    tokens = {
        "root": [
            (r"\s+", Text.Whitespace),
            (
                r"(use)(\s+)(<[a-z/_]+>)",
                bygroups(Keyword.Namespace, Text.Whitespace, Comment.PreprocFile),
            ),
            (
                r"(refer)(\s+)(to)(\s+)(<[a-z/_]+>)(\s+)(as)(\s+)([a-z_0-9]+)",
                bygroups(
                    Keyword.Namespace,
                    Text.Whitespace,
                    Keyword.Namespace,
                    Text.Whitespace,
                    Comment.PreprocFile,
                    Text.Whitespace,
                    Keyword.Namespace,
                    Text.Whitespace,
                    Name.Namespace,
                ),
            ),
            (
                r"(party|place|thing|role|moment|interval)(\s+)([A-Z][a-zA-Z0-9]*)(\s*)(\{)",
                bygroups(
                    Keyword.Reserved,
                    Text.Whitespace,
                    Name.Class,
                    Text.Whitespace,
                    Punctuation,
                ),
                "resource-declaration",
            ),
        ],
        "resource-declaration": [
            (r"\s+", Text.Whitespace),
            (
                r"(data)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "data-declaration",
            ),
            (
                r"(dnc)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "dnc-declaration",
            ),
            (
                r"(effects)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "effects-declaration",
            ),
            (
                r"(security)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "security-section",
            ),
            (r"}", Punctuation, "#pop"),
        ],
        "data-declaration": [
            (r"\s+", Text.Whitespace),
            (r"(<optional>|<computed>)", Name.Decorator),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r":", Punctuation, "property-declaration"),
            (r"}", Punctuation, "#pop"),
        ],
        "property-declaration": [
            (r"\s+", Text.Whitespace),
            (r"[a-z][a-z_0-9]*", Keyword.Type),
            (r":", Punctuation, "function-declaration"),
            (r";", Punctuation, "#pop"),
        ],
        "function-declaration": [
            (r"\s+", Text.Whitespace),
            (
                r"([a-z][a-z_0-9]*)(\s*)(\[)",
                bygroups(Name.Function, Text.Whitespace, Punctuation),
                "param-list",
            ),
            (
                r"([a-z][a-z_0-9]*)(\s*)(\()",
                bygroups(Name.Function, Text.Whitespace, Punctuation),
                "arg-list",
            ),
            (r"\(", Punctuation, "arg-list"),
            (r"value", Keyword.Reserved),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r"\|>", Operator),
            (r";", Punctuation, "#pop:2"),
        ],
        "arg-list": [
            (r"""([\"'])(?:\\\1|.)*?\1""", Literal.String),
            (r"\|>", Operator),
            (r"\s+", Text.Whitespace),
            (r"\.[0-9]+", Number.Float),
            (r"[0-9]+\.[0-9]+", Number.Float),
            (r"[0-9]+", Number.Integer),
            (r"([a-z][a-z0-9_]*)((\.[a-z][a-z0-9_]*)*)", prop_callback),
            (r",", Punctuation),
            (r"\)", Punctuation, "#pop"),
        ],
        "param-list": [
            (r"\s+", Text.Whitespace),
            (r"[a-z][a-z0-9_]*", Name.Variable),
            (r",", Punctuation),
            (r"\]", Punctuation, "#pop"),
        ],
        "dnc-declaration": [
            (r"\s+", Text.Whitespace),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r":", Punctuation, "dnc-type"),
            (r"[0-9]+", Number.Integer),
            (r"\*", Number.Integer),
            (r"\[", Punctuation),
            (r"\]", Punctuation),
            (r",", Punctuation),
            (r"}", Punctuation, "#pop"),
        ],
        "dnc-type": [
            (r"\s+", Text.Whitespace),
            (r"[A-Z][a-z_0-9]*", Name.Class),
            (r"set", Keyword.Reserved),
            (r"list", Keyword.Reserved),
            (r";", Punctuation, "#pop"),
        ],
        "effects-declaration": [
            (r"\s+", Text.Whitespace),
            (
                r"(create|modify|delete)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "effects-section",
            ),
            (r"}", Punctuation, "#pop"),
        ],
        "effects-section": [
            (r"\s+", Text.Whitespace),
            (r"}", Punctuation, "#pop"),
            (r":", Punctuation, "effects-function-declaration"),
            (r"[a-z][a-z_0-9]*", Name.Property),
        ],
        "effects-function-declaration": [
            (r"\s+", Text.Whitespace),
            (
                r"([a-z][a-z_0-9]*)(\s*)(\[)",
                bygroups(Name.Function, Text.Whitespace, Punctuation),
                "param-list",
            ),
            (
                r"([a-z][a-z_0-9]*)(\s*)(\()",
                bygroups(Name.Function, Text.Whitespace, Punctuation),
                "arg-list",
            ),
            (r"\.[0-9]+", Number.Float),
            (r"[0-9]+\.[0-9]+", Number.Float),
            (r"[0-9]+", Number.Integer),
            (r"""([\"'])(?:\\\1|.)*?\1""", Literal.String),
            (r"\(", Punctuation, "arg-list"),
            (r"value", Keyword.Reserved),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r"\|>", Operator),
            (r";", Punctuation, "#pop"),
        ],
        "security-section": [
            (r"\s+", Text.Whitespace),
            (
                r"(mutators)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "mutators-section",
            ),
            (
                r"(accessors)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "accessors-section",
            ),
            (r"\}", Punctuation, "#pop"),
        ],
        "mutators-section": [
            (r"\s+", Text.Whitespace),
            (r"\}", Punctuation, "#pop"),
            (
                r"(create|modify|delete|\*)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "bracketed-security-declaration",
            ),
            (
                r"(create|modify|delete|\*)(\s*)(:)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "security-function-declaration",
            ),
        ],
        "accessors-section": [
            (r"\s+", Text.Whitespace),
            (r"\}", Punctuation, "#pop"),
            (
                r"(list|delete|\*)(\s*)(\{)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "bracketed-security-declaration",
            ),
            (
                r"(list|delete|\*)(\s*)(:)",
                bygroups(Keyword.Reserved, Text.Whitespace, Punctuation),
                "security-function-declaration",
            ),
        ],
        "bracketed-security-declaration": [
            (r"\s+", Text.Whitespace),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r":", Punctuation, "security-function-declaration"),
            (r"\}", Punctuation, "#pop"),
        ],
        "security-function-declaration": [
            (r"\bvalue\b", Keyword.Reserved),
            (r"\b(true|false)\b", Keyword.Constant),
            (r"""([\"'])(?:\\\1|.)*?\1""", Literal.String),
            (r"\s+", Text.Whitespace),
            (r";", Punctuation, "#pop"),
            (
                r"([a-z][a-z_0-9]*)(\s*)(\()",
                bygroups(Name.Function, Text.Whitespace, Punctuation),
                "arg-list",
            ),
            (r"[a-z][a-z_0-9]*", Name.Property),
            (r"\|>", Operator),
        ],
    }
