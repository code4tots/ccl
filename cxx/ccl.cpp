/*

Reconsidering whether C++ can give me the flexibility I want.

Uses C++11 features.

Tries to follow C-style memory semantics.

Methods are kind of "wrong" in a statically typed language.

Well, virtual methods can change this, but virtual methods
are kind of a dynamically typed thing (even though Java only
has virtual methods).

*/

#include <initializer_list>
#include <iostream>
typedef long long Int;
typedef double Float;
typedef bool Bool;

// struct definitions
template <class T>
struct List {
    T * buffer;
    Int size, capacity;
};

// function declarations

// List
template <class T> void init(List<T>&);
template <class T> void init(List<T>&, Int);
// template <class T> void init(List<T>&, std::initializer_list<T>);

// function definitions
template <class T>
void init(List<T>& list) {
    init(list, 0);
}

template <class T>
void init(List<T>& list, Int initial_size) {
    list.size = initial_size;
    list.capacity = initial_size * 2 + 5;
    list.buffer = new T[list.capacity];
}

int main(int argc, char** argv) {
    
}