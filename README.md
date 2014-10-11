Computer Command Language

A programming language with a very simple execution model

Currently executable sample in 'sample.ccl'


Goals and Philosophy
====================

* Make it conceptually easy for even casual computer users to make effective use of the language.

    For instance, perhaps in the future, code like this could run:
    
        w = window {
            
            title = make-title "my videos"
            
            chart = make-pie-chart [
                ['facebook-likes', 15],
                ['retweets',       20]]
            
            like-button = make-button {
                title = "like"
                on-button-click = \ event {
                    chart.count 'facebook-likes' += 1
                }
            }
            
            retweet-button = make-button {
                title = "retweet"
                on-button-click = \ event {
                    chart.count 'rewteets' += 1
                }
            }
        }
        
        

Notes
=====

* I am considering migrating to OCaml for implementation.

* The macro semantics is different from Commom Lisp.

* Eventually, I want to move to static typing.

    My difficulty with static typing is two-folds. The first is that
    currently, I am simply leveraging Python's type system, and so from
    an implementation point of view, it is more difficult to have static
    typing.
    
    Secondly, and more fundamentally, I am still not finished designing
    the type system. Ideally, I would like to have OCaml-style type
    inference.

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

