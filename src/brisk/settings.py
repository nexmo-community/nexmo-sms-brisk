from PyInquirer import style_from_dict, Token


questions_style = style_from_dict(
    {
        Token.Separator: "#6C6C6C",
        Token.QuestionMark: "#FF9D00 bold",
        Token.Selected: "#5F819D",
        Token.Pointer: "#FF9D00 bold",
        Token.Answer: "#5F819D bold",
        Token.Question: "",
    }
)
