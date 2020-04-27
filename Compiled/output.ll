; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"True" to i8*
  %".3" = bitcast [6 x i8]* @"False" to i8*
  %"i" = alloca i32, i32 1
  store i32 1, i32* %"i"
  br label %"loop0"
loop0:
  %"i.1" = load i32, i32* %"i"
  %".6" = icmp sle i32 %"i.1", 10
  br i1 %".6", label %"loop0.if", label %"loop0.endif"
loop0.if:
  %".8" = bitcast [11 x i8]* @"fstr0" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %"i.2" = load i32, i32* %"i"
  %".10" = bitcast [4 x i8]* @"fstr1" to i8*
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", i32 %"i.2")
  %".12" = bitcast [4 x i8]* @"fstr2" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  %"i.3" = load i32, i32* %"i"
  %".14" = call i32 @"fib"(i32 %"i.3")
  %".15" = bitcast [4 x i8]* @"fstr3" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  %".17" = bitcast [2 x i8]* @"fstr4" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17")
  %"i.4" = load i32, i32* %"i"
  %".19" = add i32 %"i.4", 1
  store i32 %".19", i32* %"i"
  %"i.5" = load i32, i32* %"i"
  %".21" = icmp sle i32 %"i.5", 10
  br i1 %".21", label %"loop0", label %"afterloop0"
loop0.endif:
  ret void
afterloop0:
  br label %"loop0.endif"
}

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i32* %".1", ...) 

@"True" = internal constant [5 x i8] c"True\00"
@"False" = internal constant [6 x i8] c"False\00"
define i32 @"fib"(i32 %"a") 
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"a.2" = load i32, i32* %"a.1"
  %".4" = icmp eq i32 %"a.2", 1
  br i1 %".4", label %"entry.if", label %"entry.else"
entry.if:
  ret i32 1
entry.else:
  %"a.3" = load i32, i32* %"a.1"
  %".7" = icmp eq i32 %"a.3", 2
  br i1 %".7", label %"entry.else.if", label %"entry.else.else"
entry.endif:
  ret i32 0
entry.else.if:
  ret i32 1
entry.else.else:
  %"a.4" = load i32, i32* %"a.1"
  %".10" = sub i32 %"a.4", 1
  %".11" = call i32 @"fib"(i32 %".10")
  %"a.5" = load i32, i32* %"a.1"
  %".12" = sub i32 %"a.5", 2
  %".13" = call i32 @"fib"(i32 %".12")
  %".14" = add i32 %".11", %".13"
  ret i32 %".14"
entry.else.endif:
  br label %"entry.endif"
}

@"fstr0" = internal constant [11 x i8] c"Fibonacci \00"
@"fstr1" = internal constant [4 x i8] c"%d \00"
@"fstr2" = internal constant [4 x i8] c"is \00"
@"fstr3" = internal constant [4 x i8] c"%d \00"
@"fstr4" = internal constant [2 x i8] c"\0a\00"