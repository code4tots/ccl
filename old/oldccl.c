/* ccl

Tested with

	clang ccl.c -std=c89 -Wall -Werror -Wpedantic && ./a.out

on a OS X 10.10

*/

/* header */
typedef struct CCL_Thing CCL_Thing;

enum CCL_Type {
	CCL_NUM,
	CCL_STR,
	CCL_LIST,
	CCL_DICT
};

typedef enum CCL_Type CCL_Type;

void CCL_Init(); /* Should be called before doing anything CCL related. */

CCL_Thing * CCL_MakeNum(double value);
CCL_Thing * CCL_MakeStr(const char * value);
CCL_Thing * CCL_MakeList();
CCL_Thing * CCL_MakeDict();

void CCL_Free(CCL_Thing * me);

void CCL_CollectGarbage(CCL_Thing * stack);

CCL_Type CCL_GetType(CCL_Thing * me);
double CCL_GetNum(CCL_Thing * me);
char * CCL_GetStr(CCL_Thing * me);
int CCL_GetSizeAsInt(CCL_Thing * me);
int CCL_GetEqualAsInt(CCL_Thing * lhs, CCL_Thing * rhs);

CCL_Thing * CCL_Add(CCL_Thing * me, CCL_Thing * rhs);
CCL_Thing * CCL_Inspect(CCL_Thing * me);
CCL_Thing * CCL_GetItem(CCL_Thing * me, CCL_Thing * key);
void CCL_SetItem(CCL_Thing * me, CCL_Thing * key, CCL_Thing * value);
void CCL_PushItem(CCL_Thing * me, CCL_Thing * item);

/* implementation */
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>

typedef struct CCL_Num CCL_Num;
typedef struct CCL_Str CCL_Str;
typedef struct CCL_List CCL_List;
typedef struct CCL_Dict CCL_Dict;

struct CCL_Thing {
	CCL_Type type;
	int mark; /* for mark and sweep garbage collection */
};

struct CCL_Num {
	CCL_Thing thing;
	double value;
};

struct CCL_Str {
	CCL_Thing thing;
	char * buffer;
};

struct CCL_List {
	CCL_Thing thing;
	CCL_Thing * * buffer;
};

struct CCL_Dict {
	CCL_Thing thing;
	CCL_Thing * * buffer;
};

CCL_Thing * CCL_Malloc(CCL_Type type, size_t size);
CCL_Thing * * CCL_GetListPointer(CCL_Thing * me);
CCL_Thing * * CCL_GetDictPointer(CCL_Thing * me);

/*
Once set, CCL_OBJECT_LIST will start collecting all Thing objects that are
created. This is for facilitating garbage collection.
*/
CCL_Thing * CCL_OBJECT_LIST = NULL;

CCL_Thing * CCL_Malloc(CCL_Type type, size_t size) {
	CCL_Thing * ret = (CCL_Thing *) malloc(sizeof(size));
	ret->type = type;

	if (CCL_OBJECT_LIST != NULL) {
		assert(CCL_OBJECT_LIST->type == CCL_LIST);
		CCL_PushItem(CCL_OBJECT_LIST, ret);
	}

	return ret;
}

CCL_Thing * * CCL_GetListPointer(CCL_Thing * me) {
	assert(me->type == CCL_LIST);
	return ((CCL_List *) me)->buffer;
}

CCL_Thing * * CCL_GetDictPointer(CCL_Thing * me) {
	assert(me->type == CCL_DICT);
	return ((CCL_Dict *) me)->buffer;
}

void CCL_Init() {
	CCL_OBJECT_LIST = CCL_MakeList();
}

CCL_Thing * CCL_MakeNum(double value) {
	CCL_Num * ret = (CCL_Num *) CCL_Malloc(CCL_NUM, sizeof(CCL_Num));
	ret->value = value;
	return (CCL_Thing *) ret;
}

CCL_Thing * CCL_MakeStr(const char * value) {
	CCL_Str * ret = (CCL_Str *) CCL_Malloc(CCL_STR, sizeof(CCL_Str));
	ret->buffer = (char *) malloc(strlen(value) + 1);
	strcpy(ret->buffer, value);
	return (CCL_Thing *) ret;
}

CCL_Thing * CCL_MakeList() {
	CCL_List * ret = (CCL_List *) CCL_Malloc(CCL_LIST, sizeof(CCL_List));
	ret->buffer = (CCL_Thing * *) malloc(sizeof(CCL_Thing *));
	ret->buffer[0] = NULL;
	return (CCL_Thing *) ret;
}

CCL_Thing * CCL_MakeDict() {
	CCL_Dict * ret = (CCL_Dict *) CCL_Malloc(CCL_DICT, sizeof(CCL_Dict));
	ret->buffer = (CCL_Thing * *) malloc(sizeof(CCL_Thing *));
	ret->buffer[0] = NULL;
	return (CCL_Thing *) ret;
}

void CCL_Free(CCL_Thing * me) {
	switch (me->type) {
	case CCL_NUM:
		break;
	case CCL_STR: {
			CCL_Str * x = (CCL_Str *) me;
			free(x->buffer);
		}
		break;
	case CCL_LIST: {
			CCL_List * x = (CCL_List *) me;
			free(x->buffer);
		}
		break;
	case CCL_DICT: {
			CCL_Dict * x = (CCL_Dict *) me;
			free(x->buffer);
		}
		break;
	default:
		assert(0);
	}
	free(me);
}

void CCL_CollectGarbage(CCL_Thing * stack) {
	/* TODO */
}

CCL_Type CCL_GetType(CCL_Thing * me) {
	return me->type;
}

double CCL_GetNum(CCL_Thing * me) {
	assert(me->type == CCL_NUM);
	return ((CCL_Num *) me)->value;
}

char * CCL_GetStr(CCL_Thing * me) {
	assert(me->type == CCL_STR);
	return ((CCL_Str *) me)->buffer;
}

int CCL_GetSizeAsInt(CCL_Thing *me) {
	if (me->type == CCL_STR) {
		CCL_Str * x = (CCL_Str *) me;
		char * p = x->buffer;
		while (*p != '\0')
			p++;
		return p - x->buffer;
	} else if (me->type == CCL_LIST || me->type == CCL_DICT) {
		CCL_Thing * * p =
			(me->type == CCL_LIST) ?
			((CCL_List *) me)->buffer :
			((CCL_Dict *) me)->buffer;
		CCL_Thing * * start = p;
		while (*p != NULL) {
			p++;
		}
		return p - start;
	}
	assert(0); /* me->type is invalid */
}

int CCL_GetEqualAsInt(CCL_Thing * lhs, CCL_Thing * rhs) {
	if (lhs->type != rhs->type)
		return 0;
	switch (lhs->type) {
	case CCL_NUM:
		return CCL_GetNum(lhs) == CCL_GetNum(rhs);
	case CCL_STR:
		return strcmp(CCL_GetStr(lhs), CCL_GetStr(rhs)) == 0;
	case CCL_LIST: {
			CCL_Thing * * a = CCL_GetListPointer(lhs);
			CCL_Thing * * b = CCL_GetListPointer(rhs);
			while (*a != NULL && *b != NULL) {
				if (!CCL_GetEqualAsInt(*a, *b)) {
					return 0;
				}
				a++;
				b++;
			}
			return *a == NULL && *b == NULL;
		}
	case CCL_DICT: {
			CCL_Thing * * a = CCL_GetDictPointer(lhs);
			CCL_Thing * * b = CCL_GetDictPointer(rhs);
			while (*a != NULL && *b != NULL) {
				if (!CCL_GetEqualAsInt(*a, *b)) {
					return 0;
				}
				a++;
				b++;
			}
			return *a == NULL && *b == NULL;
		}
	}
	assert(0); /* invalid type */
}

CCL_Thing * CCL_Add(CCL_Thing * me, CCL_Thing * rhs) {
	switch (me->type) {
	case CCL_NUM:
		assert(rhs->type == CCL_NUM);
		return CCL_MakeNum(CCL_GetNum(me) + CCL_GetNum(rhs));
	case CCL_STR: {
			char * s;
			CCL_Thing * ret;
			s = malloc(sizeof(char) * (CCL_GetSizeAsInt(me) + CCL_GetSizeAsInt(rhs) + 1));
			assert(rhs->type == CCL_STR);
			strcpy(s, CCL_GetStr(me));
			strcat(s, CCL_GetStr(rhs));
			ret = CCL_MakeStr(s);
			free(s);
			return ret;
		}
	case CCL_LIST: {
			CCL_Thing * ret = CCL_MakeList();
			CCL_Thing * * p;
			assert(rhs->type == CCL_LIST);
			for (p = CCL_GetListPointer(me); *p != NULL; p++) {
				CCL_PushItem(ret, *p);
			}
			for (p = CCL_GetListPointer(rhs); *p != NULL; p++) {
				CCL_PushItem(ret, *p);
			}
			return ret;
		}
	case CCL_DICT: {
			CCL_Thing * ret = CCL_MakeDict();
			CCL_Thing * * p;
			assert(rhs->type == CCL_DICT);
			for (p = CCL_GetDictPointer(me); *p != NULL; p++) {
				CCL_Thing * key = CCL_GetItem(*p, CCL_MakeNum(0));
				CCL_Thing * value = CCL_GetItem(*p, CCL_MakeNum(1));
				CCL_SetItem(*p, key, value);
			}
			for (p = CCL_GetDictPointer(rhs); *p != NULL; p++) {
				CCL_Thing * key = CCL_GetItem(*p, CCL_MakeNum(0));
				CCL_Thing * value = CCL_GetItem(*p, CCL_MakeNum(1));
				CCL_SetItem(*p, key, value);
			}
			return ret;
		}
	}
	assert(0); /* FUBAR */
}

CCL_Thing * CCL_Inspect(CCL_Thing * me) {
	switch (me->type) {
	case CCL_NUM: {
			char s[128];
			sprintf(s, "Num(%lf)", CCL_GetNum(me));
			return CCL_MakeStr(s);
		}
	case CCL_STR:
		return CCL_Add(CCL_Add(CCL_MakeStr("Str("), me), CCL_MakeStr(")"));
	case CCL_LIST: {
			CCL_Thing * ret = CCL_MakeStr("List(");
			CCL_Thing * * p;
			for (p = CCL_GetListPointer(me); *p != NULL; p++) {
				ret = CCL_Add(ret, CCL_Inspect(*p));
			}
			ret = CCL_Add(ret, CCL_MakeStr(")"));
			return ret;
		}
	case CCL_DICT: {
			CCL_Thing * ret = CCL_MakeStr("Dict(");
			CCL_Thing * * p;
			for (p = CCL_GetDictPointer(me); *p != NULL; p++) {
				ret = CCL_Add(ret, CCL_Inspect(CCL_GetItem(*p, CCL_MakeNum(0))));
				ret = CCL_Add(ret, CCL_MakeStr(":"));
				ret = CCL_Add(ret, CCL_Inspect(CCL_GetItem(*p, CCL_MakeNum(1))));
			}
			ret = CCL_Add(ret, CCL_MakeStr(")"));
			return ret;
		}
	}
	assert(0); /* FUBAR */
}

CCL_Thing * CCL_GetItem(CCL_Thing * me, CCL_Thing * key) {
	switch (me->type) {
	case CCL_NUM:
	case CCL_STR:
		break;
	case CCL_LIST:
		assert(key->type == CCL_NUM);
		assert(CCL_GetNum(key) < CCL_GetSizeAsInt(me));
		return CCL_GetListPointer(me)[(int) CCL_GetNum(key)];
	case CCL_DICT: {
			CCL_Thing * * p = CCL_GetDictPointer(me);
			while (*p != NULL) {
				CCL_Thing * pair = *p;
				CCL_Thing * * lp = CCL_GetListPointer(pair);
				assert(pair->type == CCL_LIST && CCL_GetSizeAsInt(pair) == 2);
				if (CCL_GetEqualAsInt(lp[0], key)) {
					return lp[1];
				}
				p++;
			}
			assert(0); /* Tried to get an item that doesn't exist */
		}
	}
	assert(0); /* invalid type */
}

void CCL_SetItem(CCL_Thing * me, CCL_Thing * key, CCL_Thing * value) {
	switch (me->type) {
	case CCL_NUM:
	case CCL_STR:
		break;
	case CCL_LIST:
		assert(key->type == CCL_NUM);
		assert(CCL_GetNum(key) < CCL_GetSizeAsInt(me));
		CCL_GetListPointer(me)[(int) CCL_GetNum(key)] = value;
		return;
	case CCL_DICT: {
			CCL_Thing * * p = CCL_GetDictPointer(me);
			while (*p != NULL) {
				CCL_Thing * pair = *p;
				CCL_Thing * * lp = CCL_GetListPointer(pair);
				assert(pair->type == CCL_LIST && CCL_GetSizeAsInt(pair) == 2);
				if (CCL_GetEqualAsInt(lp[0], key)) {
					lp[1] = value;
					return;
				}
				p++;
			}
			/* Item doesn't already exist -- so add it at the end. */
			{
				CCL_Thing * pair = CCL_MakeList();
				CCL_Dict * x = (CCL_Dict *) me;
				int oldSize = CCL_GetSizeAsInt(me);
				CCL_PushItem(pair, key);
				CCL_PushItem(pair, value);
				x->buffer = realloc(x->buffer, sizeof(CCL_Thing *) * (oldSize + 2));
				x->buffer[oldSize] = pair;
				x->buffer[oldSize + 1] = NULL;
			}
			return;
		}
	}
	assert(0); /* invalid type */
}

void CCL_PushItem(CCL_Thing * me, CCL_Thing * item) {
	assert(me->type == CCL_LIST);
	{
		CCL_List * x = (CCL_List *) me;
		int oldSize = CCL_GetSizeAsInt(me);
		x->buffer = realloc(x->buffer, sizeof(CCL_Thing *) * (oldSize + 2));
		x->buffer[oldSize] = item;
		x->buffer[oldSize + 1] = NULL;
	}
}

/* main (tests) */
#include <assert.h>
#include <stdio.h>
int main() {
	CCL_Init();
	assert(CCL_GetType(CCL_MakeNum(5)) == CCL_NUM);
	{
		CCL_Thing * list = CCL_MakeList();
		assert(CCL_GetSizeAsInt(list) == 0);
		CCL_PushItem(list, CCL_MakeNum(10));
		assert(CCL_GetSizeAsInt(list) == 1);
		assert(CCL_GetEqualAsInt(CCL_GetItem(list, CCL_MakeNum(0)), CCL_MakeNum(10)));
	}
	{
		CCL_Thing * dict = CCL_MakeDict();
		assert(CCL_GetSizeAsInt(dict) == 0);
		CCL_SetItem(dict, CCL_MakeStr("hi"), CCL_MakeStr("there"));
		assert(CCL_GetSizeAsInt(dict) == 1);
		assert(CCL_GetEqualAsInt(CCL_Inspect(dict), CCL_MakeStr("Dict(Str(hi):Str(there))")));
		assert(CCL_GetEqualAsInt(CCL_GetItem(dict, CCL_MakeStr("hi")), CCL_MakeStr("there")));
	}
	printf("%s\n", CCL_GetStr(CCL_Inspect(CCL_OBJECT_LIST)));
	printf("All tests pass.\n");
}
