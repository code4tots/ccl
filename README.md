Computer Command Language

A programming language with a very simple execution model


Philosophy
==========

* Be as strict as possible without hindering expressiveness.


Rules/Wishlists
==============

A list of rules and goals that are consequences of my philosophy

* Eventually, I want to move to static typing.

    My difficulty with static typing is two-folds. The first is that
    currently, I am simply leveraging Python's type system, and so from
    an implementation point of view, it is more difficult to have static
    typing.
    
    Secondly, and more fundamentally, I am still not finished designing
    the type system. Ideally, I would like to have Haskell-like
    typeclasses and type inferencing while still permitting mutations
    like in a procedural language. The extent to which this is even
    theoretically possible is something I need to study and think more about.

* Operators

    I don't like the '+' operator and other arithmetic operators in general
    as they are syntactic sugar for arguably very specialized sitautions.
    
    These sorts of operators feel like cheap hacks to make the special case
    easier. Often they are just syntactic sugar for particular function or 
    method calls.
    
    Ideally I believe that the language should provide a more general
    framework in which these operators may be easily expressed.
    
    C is an interesting case, as a '+' function may not really be
    semantically equivalent to a '+' operator. In a naive C implementation
    a '+' operator may directly generate assembly, whereas a '+' function
    may involve all the costs that come with a true C function call.

