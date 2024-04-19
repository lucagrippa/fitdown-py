# fitdown-py
Markup language and parser for fitness logs, mainly weightlifting. A superset of [Markdown](https://en.wikipedia.org/wiki/Markdown).

Based off of [fitdown](https://github.com/datavis-tech/fitdown)

The idea is to be able to derive structured data from concise workout notes taken on a smartphone.

Here's an example of a workout log in the Fitdown format:

```
Workout February 26, 2024

5@185lb Deadlift

3x5 @ 35kg Squat

Crunches
3x20 @ 20lb 

Hammer Curl
10 @ 45.5lb each
10 @ 45.5lb each

Bench Press
10 @ 90lb 
10 @ 90lb 
10 @ 120lb TOUGH
```

The following elements are parsed:

```
[
    {
        "date": "02/26/2024",
        "exercise": "deadlift",
        "notes": "",
        "reps": 5,
        "unit": "lb",
        "weight": 185.0
    },
    {
        "date": "02/26/2024",
        "exercise": "squat",
        "notes": "",
        "reps": 5,
        "unit": "kg",
        "weight": 35.0
    },
    {
        "date": "02/26/2024",
        "exercise": "squat",
        "notes": "",
        "reps": 5,
        "unit": "kg",
        "weight": 35.0
    },
    {
        "date": "02/26/2024",
        "exercise": "squat",
        "notes": "",
        "reps": 5,
        "unit": "kg",
        "weight": 35.0
    },
    {
        "date": "02/26/2024",
        "exercise": "crunches",
        "notes": "",
        "reps": 20,
        "unit": "lb",
        "weight": 20.0
    },
    {
        "date": "02/26/2024",
        "exercise": "crunches",
        "notes": "",
        "reps": 20,
        "unit": "lb",
        "weight": 20.0
    },
    {
        "date": "02/26/2024",
        "exercise": "crunches",
        "notes": "",
        "reps": 20,
        "unit": "lb",
        "weight": 20.0
    },
    {
        "date": "02/26/2024",
        "exercise": "hammer curl",
        "notes": "each",
        "reps": 10,
        "unit": "lb",
        "weight": 45.5
    },
    {
        "date": "02/26/2024",
        "exercise": "hammer curl",
        "notes": "each",
        "reps": 10,
        "unit": "lb",
        "weight": 45.5
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "",
        "reps": 10,
        "unit": "lb",
        "weight": 90.0
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "",
        "reps": 10,
        "unit": "lb",
        "weight": 90.0
    },
    {
        "date": "02/26/2024",
        "exercise": "bench press",
        "notes": "TOUGH",
        "reps": 10,
        "unit": "lb",
        "weight": 120.0
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


## Acknowledgements

Many thanks to [Datavis Tech INC](https://github.com/datavis-tech) and [curran](https://github.com/curran) for building it in JavaScript and paving the way for me to now use this in my own notes!