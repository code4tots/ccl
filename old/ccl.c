/* ccl.c

cls && \
clang ccl.c -std=c89 -Wall -Werror -Wpedantic && \
echo "c compiler ok" && \
cp ccl.c ccl.cc && \
clang++ ccl.cc -std=c++98 -Wall -Werror -Wpedantic && \
echo 'cc compiler ok' && \
./a.out

Only 4 kinds of objects: Num, Str, List, Dict.

*/

/* header */
enum CCL_Type {
	CCL_NUM,
	CCL_STR,
	CCL_LIST,
	CCL_DICT
};
typedef enum CCL_Type CCL_Type;
typedef struct CCL_Thing CCL_Thing;
struct CCL_Thing {
	CCL_Type type;
	union {
		double num;
		char *str;
		CCL_Thing **list;
		CCL_Thing *dict; /* pointer to a list of lists */
	} data;
};

void CCL_Init();

CCL_Thing *CCL_MakeNum(double value);
CCL_Thing *CCL_MakeStr(const char *value);
CCL_Thing *CCL_MakeList();
CCL_Thing *CCL_MakeDict();

int CCL_Truthy(CCL_Thing *me);

CCL_Thing *CCL_Equal(CCL_Thing *me, CCL_Thing *x);
CCL_Thing *CCL_Size(CCL_Thing *me);
void CCL_Push(CCL_Thing *me, CCL_Thing *x);
CCL_Thing *CCL_Get(CCL_Thing *me, CCL_Thing *key);
void CCL_Set(CCL_Thing *me, CCL_Thing *key, CCL_Thing *value);
CCL_Thing *CCL_Add(CCL_Thing *me, CCL_Thing *x);

#define CCL_False CCL_MakeNum(0)
#define CCL_True CCL_MakeNum(1)

/* code */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

/* code decls */

CCL_Thing *CCL_Malloc(CCL_Type type);

/* code impls */

/* TODO: Garbage collection */

int CCL_Truthy(CCL_Thing *me) {
	switch (me->type) {
	case CCL_NUM:
		return me->data.num != 0;
	case CCL_STR:
		return me->data.str[0] != '\0';
	case CCL_LIST:
		return me->data.list[0] != NULL;
	case CCL_DICT:
		return me->data.dict->data.list[0] != NULL;
	}
}

CCL_Thing *CCL_Malloc(CCL_Type type) {
	CCL_Thing *me = (CCL_Thing *) malloc(sizeof(CCL_Thing));
	me->type = type;
	return me;
}

void CCL_Init() {
	/* TODO: Initializations */
}

CCL_Thing *CCL_MakeNum(double value) {
	CCL_Thing *me = CCL_Malloc(CCL_NUM);
	me->data.num = value;
	return me;
}

CCL_Thing *CCL_MakeStr(const char *value) {
	CCL_Thing *me = CCL_Malloc(CCL_STR);
	me->data.str = (char *) malloc(sizeof(char) *(strlen(value) + 1));
	strcpy(me->data.str, value);
	return me;
}

CCL_Thing *CCL_MakeList() {
	CCL_Thing *me = CCL_Malloc(CCL_LIST);
	me->data.list = (CCL_Thing **) malloc(sizeof(CCL_Thing) * 1);
	me->data.list[0] = NULL;
	return me;
}

CCL_Thing *CCL_MakeDict() {
	CCL_Thing *me = CCL_Malloc(CCL_DICT);
	me->data.dict = CCL_MakeList();
	return me;
}

CCL_Thing *CCL_Equal(CCL_Thing *me, CCL_Thing *x) {
	if (me->type != x->type) {
		return CCL_False;
	}
	switch (me->type) {
	case CCL_NUM:
		return me->data.num == x->data.num ? CCL_True : CCL_False;
	case CCL_STR:
		return strcmp(me->data.str, x->data.str) == 0 ? CCL_True : CCL_False;
	case CCL_LIST:
	case CCL_DICT: {
			CCL_Thing **p = me->type == CCL_LIST ? me->data.list : me->data.dict->data.list;
			CCL_Thing **q = x->type == CCL_LIST ? x->data.list : x->data.dict->data.list;
			while (*p != NULL && *q != NULL) {
				if (!CCL_Truthy(CCL_Equal(*p, *q))) {
					return CCL_False;
				}
			}
			return *p == NULL && *q == NULL ? CCL_True : CCL_False;
		}
	}
}

CCL_Thing *CCL_Size(CCL_Thing *me) {
	switch (me->type) {
	case CCL_STR:
		return CCL_MakeNum(strlen(me->data.str));
	case CCL_LIST: {
			CCL_Thing **p = me->data.list;
			while (*p != NULL)
				p++;
			return CCL_MakeNum(p - me->data.list);
		}
	case CCL_DICT:
		return CCL_Size(me->data.dict);
	default:
		assert(0); /* foobar */
	}
}

void CCL_Push(CCL_Thing *me, CCL_Thing *x) {
	switch (me->type) {
	case CCL_LIST: {
			int size = CCL_Size(me)->data.num;
			me->data.list = (CCL_Thing **) realloc(me->data.list, sizeof(CCL_Thing *) * size+2);
			me->data.list[size] = x;
			me->data.list[size+1] = NULL;
		}
		break;
	default:
		assert(0); /* foobar */
	}
}

CCL_Thing *CCL_Get(CCL_Thing *me, CCL_Thing *key) {
	switch (me->type) {
	case CCL_LIST:
		assert(key->type == CCL_NUM);
		assert(key->data.num < CCL_Size(me)->data.num);
		return me->data.list[(int) key->data.num];
	case CCL_DICT: {
			CCL_Thing * zero = CCL_MakeNum(0);
			CCL_Thing **p = me->data.dict->data.list;
			while (*p != NULL) {
				if (CCL_Truthy(CCL_Equal(key, CCL_Get(*p, zero)))) {
					return CCL_Get(*p, CCL_MakeNum(1));
				}
				p++;
			}
			assert(0); /* key is missing */
		}
	default:
		assert(0); /* foobar */
	}
}

void CCL_Set(CCL_Thing *me, CCL_Thing *key, CCL_Thing *value) {
	switch (me->type) {
	case CCL_LIST:
		assert(key->type == CCL_NUM);
		assert(key->data.num < CCL_Size(me)->data.num);
		me->data.list[(int) key->data.num] = value;
		return;
	case CCL_DICT: {
			CCL_Thing * zero = CCL_MakeNum(0);
			CCL_Thing **p = me->data.dict->data.list;
			while (*p != NULL) {
				if (CCL_Truthy(CCL_Equal(key, CCL_Get(*p, zero)))) {
					CCL_Set(*p, CCL_MakeNum(1), value);
					return;
				}
				p++;
			}
			{
				/* If key is missing just insert at end */
				CCL_Thing *pair = CCL_MakeList();
				CCL_Push(pair, key);
				CCL_Push(pair, value);
				CCL_Push(me->data.dict, pair);
			}
			return;
		}
	default:
		assert(0); /* invalid type */
	}
}

CCL_Thing *CCL_Add(CCL_Thing *me, CCL_Thing *x) {
	switch (me->type) {
	case CCL_NUM:
		assert(x->type == CCL_NUM);
		return CCL_MakeNum(me->data.num + x->data.num);
	case CCL_STR: {
			char *s;
			CCL_Thing *ret;
			assert(x->type == CCL_STR);
			s = (char *) malloc(sizeof(char) * (strlen(me->data.str) + strlen(x->data.str) + 1));
			strcpy(s, me->data.str);
			strcat(s, x->data.str);
			ret = CCL_MakeStr(s);
			free(s);
			return ret;
		}
	case CCL_LIST: {
			CCL_Thing *ret = CCL_MakeList();
			CCL_Thing **p = me->data.list;
			assert(x->type == CCL_LIST);
			while (*p != NULL) {
				printf("Adding type: %d\n", (*p)->type);
				CCL_Push(ret, *p);
				p++;
			}
			p = x->data.list;
			while (*p != NULL) {
				printf("Adding type: %d\n", (*p)->type);
				CCL_Push(ret, *p);
				p++;
			}
			printf("ret: %d\n", CCL_Get(ret, CCL_MakeNum(0))->type == CCL_STR);
			printf("ret: %d\n", CCL_Get(ret, CCL_MakeNum(0))->type);
			return ret;
		}
	case CCL_DICT:
	default:
		assert(0); /* invalid type */
	}
}

/* test (main) */
#include <stdio.h>

int main() {
	CCL_Init();
	{
		/* Make* and Equal test */
		assert(CCL_Truthy(CCL_Equal(CCL_MakeNum(5), CCL_MakeNum(5))));
		assert(CCL_Truthy(CCL_Equal(CCL_MakeStr("5"), CCL_MakeStr("5"))));
		assert(CCL_Truthy(CCL_Equal(CCL_MakeList(), CCL_MakeList())));
		assert(CCL_Truthy(CCL_Equal(CCL_MakeDict(), CCL_MakeDict())));
		assert(CCL_Truthy(CCL_Equal(CCL_Size(CCL_MakeList()), CCL_MakeNum(0))));
		assert(CCL_Truthy(CCL_Equal(CCL_Size(CCL_MakeDict()), CCL_MakeNum(0))));
	}
	{
		/* Push and Get (list) test */
		CCL_Thing *list = CCL_MakeList();
		assert(CCL_Truthy(CCL_Equal(CCL_Size(list), CCL_MakeNum(0))));
		assert(CCL_Truthy(CCL_Equal(list, CCL_MakeList())));
		CCL_Push(list, CCL_MakeStr("hi"));
		assert(CCL_Truthy(CCL_Equal(CCL_Size(list), CCL_MakeNum(1))));
		assert(CCL_Truthy(CCL_Equal(CCL_Get(list, CCL_MakeNum(0)), CCL_MakeStr("hi"))));
	}
	{
		/* CCL_Set test */
		{
			CCL_Thing *list = CCL_MakeList();
			CCL_Push(list, CCL_MakeStr("hi"));
			CCL_Set(list, CCL_MakeNum(0), CCL_MakeStr("there"));
			assert(CCL_Truthy(CCL_Equal(CCL_Get(list, CCL_MakeNum(0)), CCL_MakeStr("there"))));
		}
		{
			CCL_Thing *dict = CCL_MakeDict();
			CCL_Set(dict, CCL_MakeStr("x"), CCL_MakeStr("y"));
			assert(CCL_Truthy(CCL_Equal(CCL_Get(dict, CCL_MakeStr("x")), CCL_MakeStr("y"))));
			CCL_Set(dict, CCL_MakeStr("x"), CCL_MakeStr("yy"));
			assert(CCL_Truthy(CCL_Equal(CCL_Get(dict, CCL_MakeStr("x")), CCL_MakeStr("yy"))));
		}
	}
	{
		/* CCL_Add test */
		assert(CCL_Truthy(CCL_Equal(CCL_Add(CCL_MakeNum(5), CCL_MakeNum(6)), CCL_MakeNum(11))));
		assert(CCL_Truthy(CCL_Equal(CCL_Add(CCL_MakeStr("5"), CCL_MakeStr("6")), CCL_MakeStr("56"))));
		{
			/* list */
			CCL_Thing *a = CCL_MakeList(), *b = CCL_MakeList(), *c, *d = CCL_MakeList();
			CCL_Push(a, CCL_MakeStr("5"));
			CCL_Push(b, CCL_MakeNum(6));
			c = CCL_Add(a, b);
			printf("c: %d\n", CCL_Get(c, CCL_MakeNum(0))->type == CCL_STR);
			printf("c: %d\n", CCL_Get(c, CCL_MakeNum(0))->type);
			CCL_Push(d, CCL_MakeStr("5"));
			CCL_Push(d, CCL_MakeNum(6));
			printf("%lf\n", CCL_Size(c)->data.num);
			printf("%lf\n", CCL_Size(d)->data.num);
			printf("Typecheck: %d\n", c->type == CCL_LIST && d->type == CCL_LIST);
			printf("c: %d\n", CCL_Get(c, CCL_MakeNum(0))->type == CCL_STR);
			printf("c: %d\n", CCL_Get(c, CCL_MakeNum(0))->type);
			printf("d: %d\n", CCL_Get(d, CCL_MakeNum(0))->type == CCL_STR);
			printf("d: %d\n", CCL_Get(d, CCL_MakeNum(0))->type);
			assert(CCL_Truthy(CCL_Equal(d, c)));
		}
		{
			/* dict */
			CCL_Thing *a = CCL_MakeDict(), *b = CCL_MakeDict(), *c, *d = CCL_MakeDict();
			CCL_Set(a, CCL_MakeStr("5"), CCL_MakeStr("6"));
			CCL_Set(b, CCL_MakeNum(6), CCL_MakeNum(5));
			c = CCL_Add(a, b);
			CCL_Set(d, CCL_MakeStr("5"), CCL_MakeStr("6"));
			CCL_Set(d, CCL_MakeNum(6), CCL_MakeNum(5));
			assert(CCL_Truthy(CCL_Equal(d, c)));
		}
	}
	printf("All tests ok!\n");
}
