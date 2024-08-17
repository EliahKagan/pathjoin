# pathjoin - demo joining Windows paths like `C:foo` on the right

In a process running on Windows, each drive has a current directory, and a path like `X:` or `X:a`, beginning with a drive letter *not* followed immediately by a `\` or `/`, specifies a location relative to the current directory on that drive.

This raises the question of how to define the operation of joining such a path "under" an absolute path. For other paths, this is *mostly* straightforward:

- Taking an absolute path like `X:\a` and joining a fully relative path like `b\c` gives `X:\a\b\c`.
- Taking an absolute path like `X:\a` and joining an absolute path like `Y:\b`
gives the absolute path `Y:\b`, because if you were located at `X:\a`, this would not affect the meaning of another absolute path.
- Taking an absolute path like `X:\a` and joining a path like `\b\c` that is relative to the current drive gives `X:\b\c`, because if you are located anywhere under the `X:` drive, then `\b\c` refers to `X:\b\c`.

But there are other cases. One of them is taking an absolute path like `X:\a` and joining another such path to it. This really divides into two sub-cases:

1. The other path may be on the same drive, such as taking `X:\a` and joining `X:b`. If we follow the rule of trying to form an absolute path to the location `X:b` as it would be resolved when at the location `X:\a`, then we should form `X:\a\b`. Some path joining implementations follow this rule, while others do not and instead simply return `X:b`.
2. The other path may be on a different drive, such as taking `X:\a` and joining `Y:b`. If we were to follow the rule of trying to form an absolute path to the location `Y:b` as it would be resolved when at the location `X:\a`, then the result would depend on the current directory on `Y:`, which would have to be obtained dynamically from the system (and which could fail, if there is currently no `Y:` drive). But this behavior would also be extremely weird, since `Y:` itself is such a path: taking `X:` and joining `Y:` should not give a path like `Y:\aa\bb`, even if that is the current directory on `Y:`. Path joining implementations do not follow this rule.

This results in two potentially unintuitive effects:

- Different path joining implementations treat problems like taking `X:\a` and joining `X:b` differently. Especially to users coming from a Unix background.
- Even implementations that produce an absolute path in that case will still produce a relative path in others such as taking `X:\a` and joining `Y:b`.

In particular, it may be intuitive that taking an absolute path and joining a relative path "under" it sometimes produces a relative path.

## Examples

This repository contains a Rust program whose code is in [`src/main.rs`](src/main.rs), and a Python program whose code is at [`main.py`](main.py), that print some information about the results on Windows of taking the absolute path `C:\foo` and joining `C:bar` or `D:bar` to it.

As shown below, the Rust code is built with Rust 1.80.1, while the Python code is run in interpreters up from 3.8 up to 3.13 RC 1.

```text
C:\Users\ek\source\repos\pathjoin [main]> cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.01s
     Running `target\debug\pathjoin.exe`

left="C:\\", right="C:foo"
joined = "C:foo"
joined.is_absolute() = false
joined.is_relative() = true

left="C:\\", right="D:foo"
joined = "D:foo"
joined.is_absolute() = false
joined.is_relative() = true
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.8 main.py
Python 3.8.10

left='C:\\', right='C:foo'
oop = WindowsPath('C:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.9 main.py
Python 3.9.13

left='C:\\', right='C:foo'
oop = WindowsPath('C:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.10 main.py
Python 3.10.11

left='C:\\', right='C:foo'
oop = WindowsPath('C:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.11 main.py
Python 3.11.9

left='C:\\', right='C:foo'
oop = WindowsPath('C:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.12 main.py
Python 3.12.5

left='C:\\', right='C:foo'
oop = WindowsPath('C:/foo')
oop.is_absolute() = True
isabs(oop) = True
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

```text
C:\Users\ek\source\repos\pathjoin [main]> python3.13 main.py
Python 3.13.0rc1

left='C:\\', right='C:foo'
oop = WindowsPath('C:/foo')
oop.is_absolute() = True
isabs(oop) = True
classic = 'C:\\foo'
isabs(classic) = True

left='C:\\', right='D:foo'
oop = WindowsPath('D:foo')
oop.is_absolute() = False
isabs(oop) = False
classic = 'D:foo'
isabs(classic) = False
```

## License

Everything in this repository is licensed under [0BSD](LICENSE).
