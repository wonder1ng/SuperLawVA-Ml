import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, password } = body;

    // TODO: 실제 인증 로직 구현
    // 임시로 하드코딩된 응답 반환
    if (email === 'test@example.com' && password === 'password123') {
      return NextResponse.json({
        success: true,
        message: '로그인 성공',
        user: {
          id: 1,
          email: email,
          name: '테스트 사용자'
        }
      });
    }

    return NextResponse.json(
      { success: false, message: '이메일 또는 비밀번호가 올바르지 않습니다.' },
      { status: 401 }
    );
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { success: false, message: '서버 오류가 발생했습니다.' },
      { status: 500 }
    );
  }
} 