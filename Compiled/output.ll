; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [7 x i8]* @"fstr0" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  %".4" = bitcast [11 x i8]* @"fstr1" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4")
  %".6" = icmp eq i32 2, 3
  %".7" = bitcast [4 x i8]* @"fstr2" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i1 %".6")
  %".9" = bitcast [2 x i8]* @"fstr3" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9")
  %"a" = alloca i32, i32 1
  store i32 5, i32* %"a"
  %"a.1" = load i32, i32* %"a"
  %".12" = srem i32 8, %"a.1"
  %"b" = alloca i32, i32 1
  store i32 %".12", i32* %"b"
  %"b.1" = load i32, i32* %"b"
  %".14" = bitcast [4 x i8]* @"fstr4" to i8*
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 %"b.1")
  %".16" = bitcast [2 x i8]* @"fstr5" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16")
  %"a.2" = load i32, i32* %"a"
  %"b.2" = load i32, i32* %"b"
  %".18" = add i32 %"a.2", %"b.2"
  %".19" = bitcast [4 x i8]* @"fstr6" to i8*
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".18")
  %".21" = bitcast [2 x i8]* @"fstr7" to i8*
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@"fstr0" = internal constant [7 x i8] c"Rahul \00"
@"fstr1" = internal constant [11 x i8] c"is my name\00"
@"fstr2" = internal constant [4 x i8] c"%d \00"
@"fstr3" = internal constant [2 x i8] c"\0a\00"
@"fstr4" = internal constant [4 x i8] c"%d \00"
@"fstr5" = internal constant [2 x i8] c"\0a\00"
@"fstr6" = internal constant [4 x i8] c"%d \00"
@"fstr7" = internal constant [2 x i8] c"\0a\00"