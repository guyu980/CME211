1.1
A:
"int n" declares a variable named n with type of int.
"n=0" sets the value of variable n to 0.
"int f(void);" declares a function with no input and its return is in type of int.
"int f(void) {...}" gives the detail of this function f.

B:
Statically typed means the type of variables are defined when it is declare.
Strongly typed means it prohibits eggregious implicit conversions from disparately different data types.
C++ allows for implicit conversions between "like" types, here it can convert from int to float. 

C:
int a[10];
Static means the size of the array should be declared and can not be changed.

D:
It computes the sum of numbers from 0 to n-1.
It should declare sum=0 at first.

E:
Constructor.
It sets s to 42 and there is no return, it is used when declare a struct.



1.2
A.
int for student
long for US population
longlong for world population

B.
There will be warning for data type conversion. The tpye of v.size() is unsigned long, but i is int.

C.
It is well defined beacause srting class has default constructor and it is initialized as Null.

D.
double Dot(std::vector <double > &x, std::vector <double > &y);
It will be better to add "&" to vector variables. This will avoid copy the vector and use more memory.



1.3
const here means the pointer points to a constant and can not be changed.
*str++ means the pointer moves to the next element in str.



1.4



1.5
It will output 0. Because the last index for arr is 2. Thus there is no guarrante what arr[3] will be like.
