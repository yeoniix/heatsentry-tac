//프론트엔드에 군인목록을 띄우고 싶을 때 fetchSoldiers()함수를 호출하면서 서버에 가서 데이터를 깔끔하게 받아오자
import axios from "axios";
import type { Soldier } from "../types/soldier";

//백엔드 서버에 요청을 보내 군인의 정보 가져오기 
//서버와 통신하기 위한 도구 axios

const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchSoldiers(): Promise<Soldier[]> {
  const response = await axios.get<Soldier[]>(`${API_BASE_URL}/api/soldiers`);
  return response.data;
}
//다른 파일이 이 함수를 쓸 수 있도록 export사용. 데이터가 올 때까지 기다려야 하므로 async(비동기)사용
//Promise<Soldier[]> => 함수가 최종적으로 군인 정보가 담긴 배열을 반환할것
//response 변수에 /api/soldiers라는 주소에서 데이터를 달라고 서버에 GET요청하고 그 결과를 담는다.

