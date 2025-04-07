#if(a%2==0):
   # print("The number" ,a ," is even")
#else:
    #print("the numbefr is odd")
#if(a>b&a>c):
   # print(a," is gretest")
#elif(b>a&b>c):
   # print(b)
#else:
   # print(c)


# import math
# a=int(input("enter 1st number "))
# b=int(input("enter 2nd number "))
# c=int(input("enter 3rd number "))
   
# d=((b*b)-4*a*c)
# if(d==0):
#     r1=-b/2*a
#     r2=-b/2*a
#     print(r1, r2, "roots are real and equal")

# elif(d>0):
#     r1=(-b+(math.sqrt(d)))/2*a
#     r2=(-b-(math.sqrt(d)))/2*a
#     print(r1, r2, "roots are real and different")
# else:
#     print("roots are imaginari")



# a=int(input("enter the number: "))

# for i in range(1,11):
#     table=i*a
#     print(5 ,"*",i," = ",table)
# fact=1
# while(a!=0):
#     fact*=a
#     a=a-1
# print(fact)

# a=int(input("enter the 1st number: "))
# b=int(input("enter the 2nd number: "))
# def swap(a,b):
#     x=a
#     a=b
#     b=x
#     print(a,b)
# swap(a,b)










# def multi(a,b):
#     ml=a*b
#     return ml
# def add(a,b):
#     ad=a+b
#     return ad
# def diff(a,b):
#     dif=a-b
#     return dif
# a=int(input("first number: " ))
# b=int(input("second number: " ))
# print("multification of two number ",multi(a,b))
# print("addiation ",add(a,b))
# print("subtraction", diff(a,b))



def fact(a):
   if(a==1):
      return 1
   else:
      return (a*fact(a-1))
a=int(input("enter the number: " ))
print("factorial",fact(a))
         



