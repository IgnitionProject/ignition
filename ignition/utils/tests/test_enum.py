from ignition import Enum

def test_Enum ():
    Colours = Enum('red', 'blue', 'green')
    Weekdays = Enum('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

    pizza_night = Weekdays[4]
    game_night = Weekdays['mon']
    shirt_colour = Colours.green

    assert(pizza_night == Weekdays.fri)
    assert(game_night == Weekdays[0])
    assert(shirt_colour > Colours.red)
    assert(shirt_colour != "green")

    multi = Enum(('foo', 'bar'), 'baz')
    assert(multi.foo == multi.bar)
