; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = sub i32 2, 1
  %".3" = add i32 3, %".2"
  %".4" = bitcast [5 x i8]* @"fstr0" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".3")
  %".6" = sub i32 5, 1
  %".7" = add i32 4, %".6"
  %".8" = bitcast [5 x i8]* @"fstr1" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".7")
  %".10" = add i32 5, 1
  %".11" = sub i32 4, %".10"
  %".12" = bitcast [5 x i8]* @"fstr2" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@"fstr0" = internal constant [5 x i8] c"%i \0a\00"
@"fstr1" = internal constant [5 x i8] c"%i \0a\00"
@"fstr2" = internal constant [5 x i8] c"%i \0a\00"