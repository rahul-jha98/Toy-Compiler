; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"False" to i8*
  %".3" = bitcast [5 x i8]* @"True" to i8*
  %".4" = bitcast [4 x i8]* @"int" to i8*
  %"a" = alloca i32, i32 1
  store i32 5, i32* %"a"
  %"b" = alloca i32, i32 1
  store i32 5, i32* %"b"
  %"a.1" = load i32, i32* %"a"
  %"b.1" = load i32, i32* %"b"
  %".7" = call i32 @"updatevalue"(i32 %"a.1", i32 %"b.1")
  %".8" = bitcast [43 x i8]* @"fstr2" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %"a.2" = load i32, i32* %"a"
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %"a.2")
  %"b.2" = load i32, i32* %"b"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %"b.2")
  %".12" = bitcast [2 x i8]* @"fstr3" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"True" = internal constant [5 x i8] c"True\00"
@"False" = internal constant [6 x i8] c"False\00"
@"int" = internal constant [4 x i8] c"%d \00"
define i32 @"updatevalue"(i32 %"a", i32 %"b") 
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32
  store i32 %"b", i32* %"b.1"
  %".6" = bitcast [6 x i8]* @"False" to i8*
  %".7" = bitcast [5 x i8]* @"True" to i8*
  %".8" = bitcast [4 x i8]* @"int" to i8*
  %"a.2" = load i32, i32* %"a.1"
  %".9" = mul i32 %"a.2", 2
  store i32 %".9", i32* %"a.1"
  %"b.2" = load i32, i32* %"b.1"
  %".11" = sdiv i32 %"b.2", 2
  store i32 %".11", i32* %"b.1"
  %".13" = bitcast [39 x i8]* @"fstr0" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13")
  %"a.3" = load i32, i32* %"a.1"
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %"a.3")
  %"b.3" = load i32, i32* %"b.1"
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %"b.3")
  %".17" = bitcast [2 x i8]* @"fstr1" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17")
  ret i32 0
}

@"fstr0" = internal constant [39 x i8] c"The values of a and b in functions is \00"
@"fstr1" = internal constant [2 x i8] c"\0a\00"
@"fstr2" = internal constant [43 x i8] c"The values of a and b outside function is \00"
@"fstr3" = internal constant [2 x i8] c"\0a\00"