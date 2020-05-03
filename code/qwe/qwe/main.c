#include <stdio.h>

int power(int a, int b) {
    int ans = 1;
    for (int i = 0; i < b; ++i) {
        ans *= a;
    }
    return ans;
}

int intTobinary(int a) {
    int ans = 0;
    while (a > 0){
        if ((a & 1) == 0) {
            ans = ans * 10;
        }
        else {
            ans = ans * 10 + 1;
        }
        a >>= 1;
    }
    return ans;
}

int binaryToInt(int binary) {
    int p = 0;
    int ans = 0;
    while (binary > 0) {
        ans += (binary % 10) * power(2, p);
        binary /= 10;
        ++p;
    }
    return ans;
}

int getOctetOfMask(int cntBits) {
    int ans = 0;
    for (int i = 0; i < cntBits; ++i){
        ans = ans * 10 + 1;
    }
    ans *= power(10, 8 - cntBits);
    return ans;
}

int factorial(int n) {
    if (n == 0) {
        return 1;
    }
    else {
        return n * factorial(n - 1);
    }
}


void ipCalc() {
    int cntBitsOfMask;
    int octetsOfIp[4];
    scanf("%d.%d.%d.%d/%d", &octetsOfIp[3], &octetsOfIp[2], &octetsOfIp[1], &octetsOfIp[0], &cntBitsOfMask);
    int octetsOfMask[4];
    for (int i = 3; i >= 0; --i) {
        if (cntBitsOfMask >= 8) {
            octetsOfMask[i] = binaryToInt(11111111);
            cntBitsOfMask -= 8;
        }
        else if (cntBitsOfMask > 0 && cntBitsOfMask < 8){
            octetsOfMask[i] = binaryToInt(getOctetOfMask(cntBitsOfMask));
            cntBitsOfMask = 0;
        }
        else {
            octetsOfMask[i] = 0;
        }
    }
    int octetsOfNetwork[4];
    for (int i = 0; i < 4; ++i){
        octetsOfNetwork[i] = octetsOfIp[i] & octetsOfMask[i];
    }
    printf("%d.%d.%d.%d", octetsOfNetwork[3], octetsOfNetwork[2], octetsOfNetwork[1], octetsOfNetwork[0]);
}

void f1() {
    char c = 65;
    unsigned char uc;
    uc = 5;
    printf("%d %c\n", c, c);
    int i;
    unsigned int ui;
    long int li;
    float f;
    double d;

    i = (int) c;
    printf("%d\n", i);

    int mas1[] = {1, 2, 3};
    int mas2[3] ={2, 3, 4};
    int mas3[3] = {0};
    printf("%d %d %d\n", mas3[0], mas3[1], mas3[2]);

    enum gender{
        male,
        female
    };
    enum bool{
        FALSE,
        TRUE
    };
    printf("%d %d\n", male, female);

    struct student{
        int age;
        int height;
        int groupNumber;
    };

    struct student s;
    s.age = 20;
    s.height = 183;
    s.groupNumber = 123;
    struct student s2 = {21, 180, 123};
    printf("Student age: %d; student height: %d; student group number: %d\n", s.age, s.height, s.groupNumber);
    printf("Student age: %d; student height: %d; student group number: %d\n", s2.age, s2.height, s2.groupNumber);


    typedef union integer{
        int i;
        char c;
        unsigned long long ll;
    } integer;

    integer a;
    a.ll = 1231231233;
    printf("%x %x %llu", a.c, a.i, a.ll);
}

void f2() {
    int a;
    scanf("%d", &a);
    printf("a=%d\n", a);
}

void f3() {
    int a = 5;
    int b = 3;
    printf("%d * %d = %d\n", a, b, a * b);
    printf("%d + %d = %d\n", a, b, a + b);
    printf("%d - %d = %d\n", a, b, a - b);
    printf("%d / %d = %d\n", a, b, a / b);
    printf("%d %% %d = %d\n", a, b, a % b);
    b = a;
    printf("++%d = %d\n", a, ++b);
    b = a;
    printf("%d++ = %d\n", a, b++);
    b = a;
    printf("-%d = %d\n", a, -b);
    a = 5;
    b = 3;
    printf("%d and %d = %d\n", a, b, a & b);
    printf("%d or %d = %d\n", a, b, a | b);
    unsigned char c1 = 125;
    unsigned char c2 = ~c1;
    printf("not %d = %d\n", c1, c2);
    a = 5;
    printf("%d >> %d = %d\n", a, 2, a >> 2);
    printf("%d << %d = %d\n", a, 2, a << 2);
}

void f4() {
    int a, b;
    scanf("%d %d", &a, &b);
    if (a > b) {
        printf("%d > %d\n", a, b);
    }
    else {
        printf("%d <= %d\n", a, b);
    }
    int c;
    scanf("%d", &c);
    switch (c) {
        case 1:
            printf(":)\n");
            break;
        case 2:
            printf(":(\n");
            break;
        default:
            printf("Incorrect input!\n");
    }


    for (int i = 0; i < 6; ++i) {
        printf("%d\n", i);
    }

    int i = 0;
    while (i < 7){
        printf("%d\n", i * i);
        ++i;
    }

    i = -1;

    do {
        printf("%d", i);
    } while (i > 0);
}

int main() {
//    f1();
//    f2();
//    f3();
//    f4();
//    printf("%d ^ %d = %d\n", 3, 4, power(3, 4));
//    printf("!%d = %d", 5, factorial(5));
    ipCalc();
    return 0;
}
