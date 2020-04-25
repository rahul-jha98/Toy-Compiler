; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %"a" = alloca i32, i32 1
  store i32 2, i32* %"a"
  %"a.1" = load i32, i32* %"a"
  %".3" = icmp eq i32 %"a.1", 2
  br i1 %".3", label %"entry.if", label %"entry.else"
entry.if:
  %".5" = bitcast [4 x i8]* @"fstr0" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".5", i32 5)
  %".7" = bitcast [2 x i8]* @"fstr1" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7")
  %"a.2" = load i32, i32* %"a"
  %"b" = alloca i32, i32 1
  store i32 %"a.2", i32* %"b"
  %".10" = mul i32 4, 8
  %".11" = bitcast [4 x i8]* @"fstr2" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 %".10")
  %".13" = bitcast [2 x i8]* @"fstr3" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13")
  %"b.1" = load i32, i32* %"b"
  %".15" = bitcast [4 x i8]* @"fstr4" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %"b.1")
  %".17" = bitcast [2 x i8]* @"fstr5" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17")
  br label %"entry.endif"
entry.else:
  %"a.3" = load i32, i32* %"a"
  %".20" = icmp eq i32 %"a.3", 3
  br i1 %".20", label %"entry.else.if", label %"entry.else.else"
entry.endif:
  ret void
entry.else.if:
  %"a.4" = load i32, i32* %"a"
  %".22" = add i32 %"a.4", 1
  %"b.2" = alloca i32, i32 1
  store i32 %".22", i32* %"b.2"
  %"b.3" = load i32, i32* %"b.2"
  %".24" = bitcast [4 x i8]* @"fstr6" to i8*
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".24", i32 %"b.3")
  %".26" = bitcast [2 x i8]* @"fstr7" to i8*
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26")
  br label %"entry.else.endif"
entry.else.else:
  %".29" = bitcast [5 x i8]* @"fstr8" to i8*
  %".30" = call i32 (i8*, ...) @"printf"(i8* %".29")
  %".31" = bitcast [2 x i8]* @"fstr9" to i8*
  %".32" = call i32 (i8*, ...) @"printf"(i8* %".31")
  br label %"entry.else.endif"
entry.else.endif:
  br label %"entry.endif"
}

declare i32 @"printf"(i8* %".1", ...) 

@"fstr0" = internal constant [4 x i8] c"%d \00"
@"fstr1" = internal constant [2 x i8] c"\0a\00"
@"fstr2" = internal constant [4 x i8] c"%d \00"
@"fstr3" = internal constant [2 x i8] c"\0a\00"
@"fstr4" = internal constant [4 x i8] c"%d \00"
@"fstr5" = internal constant [2 x i8] c"\0a\00"
@"fstr6" = internal constant [4 x i8] c"%d \00"
@"fstr7" = internal constant [2 x i8] c"\0a\00"
@"fstr8" = internal constant [5 x i8] c"else\00"
@"fstr9" = internal constant [2 x i8] c"\0a\00"