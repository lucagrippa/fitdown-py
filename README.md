# fitdown-py
Markup language and parser for fitness logs, mainly weightlifting. A superset of [Markdown](https://en.wikipedia.org/wiki/Markdown).

Based off of [fitdown](https://github.com/datavis-tech/fitdown)

The idea is to be able to derive structured data from concise workout notes taken on a smartphone.

Here's an example of a workout log in the Fitdown format:

```
Workout February 27, 2024

5@185 Deadlift

Snatch
Up to technique bar + 35lb each side

Clean and Jerk
Up to 145lb

Squat
3x5@165
  
Bench Press
3x5 @ 170lb
  
Deadlift
5 @ 185
5 @ 255 TOUGH
```

The following elements are parsed:

```
[
    {
        "date": "02/27/2024",
        "exercise": "Deadlift",
        "poundage": 185,
        "reps": 5
    },
    {
        "exercise": "Snatch",
        "notes": "Up to technique bar + 35lb each side",
        "poundage": 35
    },
    {
        "exercise": "Clean and Jerk",
        "notes": "Up to 145lb",
        "poundage": 145
    },
    {
        "date": "02/27/2024",
        "exercise": "Squat",
        "poundage": 165,
        "reps": 5
    },
    {
        "date": "02/27/2024",
        "exercise": "Squat",
        "poundage": 165,
        "reps": 5
    },
    {
        "date": "02/27/2024",
        "exercise": "Squat",
        "poundage": 165,
        "reps": 5
    },
    {
        "date": "02/27/2024",
        "exercise": "Deadlift",
        "poundage": 185,
        "reps": 5
    },
    {
        "date": "02/27/2024",
        "exercise": "Deadlift",
        "notes": "TOUGH",
        "poundage": 255,
        "reps": 5
    }
]
```

## Workout Date
Example:
```
Workout September 16, 2020
```

It triggers on the term "Workout", and requires this very specific date format.

All exercises that follow a workout date line have that data associated with it.

## Exercises with Sets & Reps
Example:

```
Deadlift
5@185
5@255
```

This notation allows you to track a specific exercise and its sets and reps (repititions) with poundages.

The first line of the group specifies the exercise, e.g. `Deadlift`.

Subsequent lines indicate one set each, where the structure is `${reps}@${poundage}`. For example `5@185` means 5 reps at 185 pounds. This triggers on the `@` symbol.

## Single Line Exercises
Example:
```
5@185 Deadlift
```
You can also define an entire exercise on a single line. The above example is equivalent to:

```
Deadlift
5@185
```

However, be careful to include an empty line before the single line exercise, otherwise it will be grouped with the previous exercise.

## Exercises with Multiplied Sets & Reps

Example:
```
Squat
3x5@165
```

You can use a multiplier like `3x` or `4x` as a concise alternative to repeating the same sets. It triggers on `x` or `X`.

The above example is equivalent to:

```
Squat
5@165
5@165
5@165
```

## Notes

Example:

```
Deadlift
5@185
5@255 TOUGH
```

You can add any text after a set to add notes to it. In this case the notes `TOUGH` are associated to the second Deadlift set.

## Loosely Formatted Exercises
Examples:
```
Snatch
Up to technique bar + 35lb each side
```
```
Clean and Jerk
Up to 145lb
```
It triggers on "lb". Exercise and poundage are parsed, and the entire line that includes "lb" is treated as notes.

## Acknowledgements

Many thanks to [Datavis Tech INC](https://github.com/datavis-tech) and [curran](https://github.com/curran) for building it in JavaScript and paving the way for me to now use this in my own notes!