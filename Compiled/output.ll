; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"True" to i8*
  %".3" = bitcast [6 x i8]* @"False" to i8*
  %".4" = bitcast [3 x i8]* @"int" to i8*
  %"a" = alloca i32, i32 1
  store i32 0, i32* %"a"
  %".6" = bitcast [36 x i8]* @"fstr0" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6")
  %".8" = bitcast [2 x i8]* @"fstr1" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %".10" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* %"a")
  %"i" = alloca i32, i32 1
  store i32 1, i32* %"i"
  br label %"loop0"
loop0:
  %"i.1" = load i32, i32* %"i"
  %".13" = icmp slt i32 %"i.1", 11
  br i1 %".13", label %"loop0.if", label %"loop0.endif"
loop0.if:
  %"a.1" = load i32, i32* %"a"
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %"a.1")
  %".16" = bitcast [4 x i8]* @"fstr2" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16")
  %"i.2" = load i32, i32* %"i"
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %"i.2")
  %".19" = bitcast [4 x i8]* @"fstr3" to i8*
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19")
  %"a.2" = load i32, i32* %"a"
  %"i.3" = load i32, i32* %"i"
  %".21" = mul i32 %"a.2", %"i.3"
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".21")
  %".23" = bitcast [2 x i8]* @"fstr4" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23")
  %"i.4" = load i32, i32* %"i"
  %".25" = add i32 %"i.4", 1
  store i32 %".25", i32* %"i"
  %"i.5" = load i32, i32* %"i"
  %".27" = icmp slt i32 %"i.5", 11
  br i1 %".27", label %"loop0", label %"afterloop0"
loop0.endif:
  %".30" = icmp eq i32 2, 10
  br i1 %".30", label %"loop0.endif.if", label %"loop0.endif.else"
afterloop0:
  br label %"loop0.endif"
loop0.endif.if:
  %".32" = call i32 (i8*, ...) @"printf"(i8* %".2")
  br label %"loop0.endif.endif"
loop0.endif.else:
  %".34" = call i32 (i8*, ...) @"printf"(i8* %".3")
  br label %"loop0.endif.endif"
loop0.endif.endif:
  %".36" = bitcast [2 x i8]* @"fstr5" to i8*
  %".37" = call i32 (i8*, ...) @"printf"(i8* %".36")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"True" = internal constant [5 x i8] c"True\00"
@"False" = internal constant [6 x i8] c"False\00"
@"int" = internal constant [3 x i8] c"%d\00"
@"fstr0" = internal constant [36 x i8] c"Enter a number whose table you need\00"
@"fstr1" = internal constant [2 x i8] c"\0a\00"
@"fstr2" = internal constant [4 x i8] c" * \00"
@"fstr3" = internal constant [4 x i8] c" = \00"
@"fstr4" = internal constant [2 x i8] c"\0a\00"
@"fstr5" = internal constant [2 x i8] c"\0a\00"