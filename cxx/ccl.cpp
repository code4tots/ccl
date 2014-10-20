/*

Reconsidering whether C++ can give me the flexibility I want.

Uses C++11 features.

Tries to follow C-style memory semantics.

*/

#include <initializer_list>
#include <iostream>
typedef long long Int;
typedef double Float;
typedef bool Bool;

template <class T>
struct List {
    T * _buffer;
    Int _size, _capacity;
    
    void init(Int reserved_size) {
        _size = reserved_size;
        _capacity = _size * 2 + 5;
        _buffer = new T[_capacity];
    }
    
    void init() {
        init(0);
    }
    
    void init(std::initializer_list<T> items) {
        init();
        for (auto i = items.begin(); i != items.end(); ++i) {
            push(*i);
        }
    }
    
    void deinit() {
        delete[] _buffer;
    }
    
    T& operator[](Int i) {
        return _buffer[i];
    }
    
    Int size() {
        return _size;
    }
    
    Bool empty() {
        return size() == 0;
    }
    
    void push(T t) {
        if (_size == _capacity)
            _reallocate_buffer(_capacity * 2);
        _buffer[_size++] = t;
    }
    
    T pop() {
        if (_size > 10 && 8 * _size < _capacity)
            _reallocate_buffer(_capacity / 2);
        return _buffer[--_size];
    }
    
    void _reallocate_buffer(Int new_capacity) {
        T * new_buffer = new T[new_capacity];
        for (Int i = 0; i < _size; i++)
            new_buffer[i] = _buffer[i];
        delete[] _buffer;
        _buffer = new_buffer;
        _capacity = new_capacity;
    }
    
    T * begin() {
        return _buffer;
    }
    
    T * end() {
        return _buffer + _size;
    }
};

template <class T>
std::ostream& std::operator<<(std::ostream& out, List<T>& list) {
    out << '[';
    for (auto i = list.begin(); i != list.end(); ++i) {
        if (i != list.begin())
            out << ", ";
        out << *i;
    }
    out << ']';
}

Int hash(Int i) {
    return i;
}

Int hash(Float f) {
    return (Int) f;
}

int main(int argc, char** argv) {
    List<Int> list;
    list.init({1, 2, 3});
    std::cout << list << std::endl;
    
    while (!list.empty())
        std::cout << list.pop() << std::endl;
    
    return 0;
}