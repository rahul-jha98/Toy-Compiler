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
  %".6" = bitcast [2 x i8]* @"fstr2" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6")
  %".8" = bitcast [7 x i8]* @"fstr3" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %".10" = icmp eq i32 5, 2
  %".11" = bitcast [4 x i8]* @"fstr4" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i1 %".10")
  %".13" = add i32 4, 2
  %".14" = add i32 %".13", 5
  %".15" = bitcast [4 x i8]* @"fstr5" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".14")
  %".17" = bitcast [2 x i8]* @"fstr6" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@"fstr0" = internal constant [7 x i8] c"Rahul \00"
@"fstr1" = internal constant [11 x i8] c"is my name\00"
@"fstr2" = internal constant [2 x i8] c"\0a\00"
@"fstr3" = internal constant [7 x i8] c"Rahul \00"
@"fstr4" = internal constant [4 x i8] c"%d \00"
@"fstr5" = internal constant [4 x i8] c"%d \00"
@"fstr6" = internal constant [2 x i8] c"\0a\00"