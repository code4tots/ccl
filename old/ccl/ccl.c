/* ccl.c

cls && \
clang ccl.c -std=c89 -Wall -Werror -Wpedantic && \
echo "c compiler ok" && \
cp ccl.c ccl.cc && \
clang++ ccl.cc -std=c++98 -Wall -Werror -Wpedantic && \
rm ccl.cc && \
echo 'cc compiler ok' && \
./a.out

*/
#define CCL_STR 0
#define CCL_LIST 1

typedef struct CCL_Object CCL_Object;
struct CCL_Object {
	int type, size;
	union {
		char *s;
		CCL_Object **l;
	} d;
};

extern char *CCL_ERROR_MESSAGE;

CCL_Object *CCL_MakeStr(const char *s);
CCL_Object *CCL_MakeList();
double CCL_Num(CCL_Object *me);
int CCL_StrEqual(CCL_Object *lhs, CCL_Object *rhs);
int CCL_ListEqual(CCL_Object *lhs, CCL_Object *rhs);
int CCL_Equal(CCL_Object *lhs, CCL_Object *rhs);
CCL_Object *CCL_AddStr(CCL_Object *lhs, CCL_Object *rhs);
CCL_Object *CCL_InspectStr(CCL_Object *me);
CCL_Object *CCL_InspectList(CCL_Object *me);
CCL_Object *CCL_Inspect(CCL_Object *me);

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

/* If not NULL, indicates an error */
char *CCL_ERROR_MESSAGE = NULL;

static void CCL_CreateErrorMessageBuffer(int size) {
	CCL_ERROR_MESSAGE = (char*) malloc(sizeof(char) * size);
}

CCL_Object *CCL_MakeStr(const char *s) {
	CCL_Object *me = (CCL_Object*) malloc(sizeof(CCL_Object));
	me->type = CCL_STR;
	me->d.s = (char*) malloc(sizeof(char) * strlen(s));
	strcpy(me->d.s, s);
	me->size = strlen(s);
	return me;
}

CCL_Object *CCL_MakeList() {
	CCL_Object *me = (CCL_Object*) malloc(sizeof(CCL_Object));
	me->type = CCL_LIST;
	me->d.l = NULL;
	me->size = 0;
	return me;
}

/* convert a Str to a double */
double CCL_Num(CCL_Object *me) {
	char *endptr;
	double ret;
	assert(me->type == CCL_STR);
	ret = strtod(me->d.s, &endptr);
	if (endptr == me->d.s) {
		CCL_CreateErrorMessageBuffer(100 + strlen(me->d.s));
		sprintf(CCL_ERROR_MESSAGE, "Could not convert to number: %s", me->d.s);
	}
	return ret;
}

int CCL_StrEqual(CCL_Object *lhs, CCL_Object *rhs) {
	assert(lhs->type == CCL_STR);
	assert(rhs->type == CCL_STR);
	return strcmp(lhs->d.s, rhs->d.s) == 0;
}

int CCL_ListEqual(CCL_Object *lhs, CCL_Object *rhs) {
	CCL_Object **a, **b;
	assert(lhs->type == CCL_LIST);
	assert(rhs->type == CCL_LIST);
	for (a = lhs->d.l, b = rhs->d.l; *a != NULL && *b != NULL; a++, b++) {
		if (!CCL_Equal(*a, *b)) {
			return 0;
		}
	}
	return a == NULL && b == NULL;
}

int CCL_Equal(CCL_Object *lhs, CCL_Object *rhs) {
	return (lhs->type != rhs->type) ? 0 :
			(lhs->type == CCL_STR) ? CCL_StrEqual(lhs, rhs) :
			CCL_ListEqual(lhs, rhs);
}

/* Concatenates two strings and returns a new one */
CCL_Object *CCL_AddStr(CCL_Object *lhs, CCL_Object *rhs) {
	CCL_Object *ret = CCL_MakeStr(lhs->d.s);
	assert(lhs->type == CCL_STR);
	assert(rhs->type == CCL_STR);
	ret->size = lhs->size + rhs->size;
	ret->d.s = (char*) realloc(ret->d.s, sizeof(char) * (ret->size + 1));
	strcat(ret->d.s + lhs->size, rhs->d.s);
	return ret;
}

CCL_Object *CCL_InspectStr(CCL_Object *me) {
	return CCL_AddStr(
			CCL_MakeStr("Str("),
			CCL_AddStr(me, CCL_MakeStr(")")));
}

CCL_Object *CCL_InspectList(CCL_Object *me) {
	CCL_Object *ret = CCL_MakeStr("List(");
	CCL_Object **p;
	assert(me->type == CCL_LIST);
	for (p = me->d.l; *p != NULL; p++) {
		ret = CCL_AddStr(ret, CCL_Inspect(*p));
	}
	return ret;
}

CCL_Object *CCL_Inspect(CCL_Object *me) {
	return me->type == CCL_STR ? CCL_InspectStr(me) : CCL_InspectList(me);
}

int main(int argc, char **argv) {
	assert(CCL_Equal(
			CCL_MakeStr("Hello world!"),
			CCL_AddStr(
				CCL_MakeStr("Hello "),
				CCL_MakeStr("world!"))));
}
