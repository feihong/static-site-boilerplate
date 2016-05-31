
$content = $('#content')

section = (title) -> $('<h4>').text(title).appendTo($content)
print = (text) -> $('<p>').text(text).appendTo($content)

#=============================================================================

section 'Comprehensions'

numbers = [1, 3, 5, 6, 7, 8, 9, 11, 12, 14, 16, 17]
print [(n*2 + 1) for n in numbers when n > 10]
