
$content = $('#content')

section = (title) -> $('<h4>').text(title).appendTo($content)
print = (text) -> $('<p>').text(text).appendTo($content)

#=============================================================================

section 'String interpolation'

name = 'Dr Groot'
title = 'plant matter expert'

print "Hey, #{name} is our resident #{title}."

section 'Comprehensions'

numbers = [1, 3, 5, 6, 7, 8, 9, 11, 12, 14, 16, 17]
print [(n*2 + 1) for n in numbers when n > 10]

section 'Existential operator'

obj1 = artist:
  name: 'Marty'
  latestAlbum:
      title: 'Back in Time'

print obj1.artist?.latestAlbum?.title

obj2 = artist:
  name: 'Marty'
  latestAlbum: null

print obj2.artist?.latestAlbum?.title
