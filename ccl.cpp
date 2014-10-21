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
typedef int Int;
typedef double Float;
typedef bool Bool;

// struct definitions
template <class T>
struct List {
    T * buffer;
    Int size, capacity;
};

template <class K, class V>
struct Map {
    
};

// function declarations

// List
template <class T> void init(List<T>&);
template <class T> void init(List<T>&, Int);
template <class T> void init(List<T>&, std::initializer_list<T>);
template <class T> void deinit(List<T>&);
template <class T> void push(List<T>&, T);
template <class T> T pop(List<T>&);
template <class T> void _reallocate(List<T>&, Int);
template <class T> T* begin(List<T>&);
template <class T> T* end(List<T>&);
template <class T> std::ostream& std::operator<<(std::ostream&, List<T>&);

// Map
template <class K, class V> void init(Map<K,V>&);

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

template <class T>
void init(List<T>& list, std::initializer_list<T> items) {
    init(list);
    for (auto i = items.begin(); i != items.end(); ++i)
        push(list, *i);
}

template <class T>
void deinit(List<T>& list) {
    delete[] list.buffer;
}

template <class T>
void push(List<T>& list, T t) {
    if (list.size == list.capacity)
        _reallocate(list, list.size * 2);
    list.buffer[list.size++] = t;
}

template <class T>
T pop(List<T>& list) {
    if (list.size > 10 && 8 * list.size < list.capacity)
        _reallocate(list, list.size / 2);
    return list.buffer[--list.size];
}

template <class T> T pop(List<T>&);

template <class T>
void _reallocate(List<T>& list, Int new_capacity) {
    T * new_buffer = new T[new_capacity];
    for (Int i = 0; i < list.size; ++i)
        new_buffer[i] = list.buffer[i];
    delete[] list.buffer;
    list.buffer = new_buffer;
    list.capacity = new_capacity;
}

template <class T>
T * begin(List<T>& list) {
    return list.buffer;
}

template <class T>
T * end(List<T>& list) {
    return list.buffer + list.size;
}

template <class T>
std::ostream& std::operator<<(std::ostream& out, List<T>& list) {
    out << '[';
    for (auto i = begin(list); i != end(list); ++i) {
        if (i != begin(list))
            out << ", ";
        out << *i;
    }
    out << ']';
}

int main(int argc, char** argv) {
    List<Int> list;
    init(list, {1,2,3});
    std::cout << list << std::endl;
}
