# redis_study_fastAPI
## 목적
redis를 활용해서 db-caching을 알아본다.

</br>

## 환경
- 서버 프레임워크 : fastAPI
- python : 3.9.12
- DB : MySQL(8.0.30) (ENGINE=InnoDB)
- Redis 6.2.7
- redis-stack-server 사용

</br></br>

# DB

## <Table 정보>

</br>

### 1. user_info
| uid(primary_key) | id | pw | nick_name | reg_date | update_date |
|------------------|----|----|-----------|----------|-------------|
</br>

### 2. favorites
| id(primary_key) | station_id | uid | reg_date |
|-----------------|------------|-----|----------|
</br>

### 3. session
| session_id(primary_key) | uid | reg_date | expire_date |
|-------------------------|-----|----------|-------------|
</br></br></br>

## Table Generating Query

```
CREATE TABLE `user_info` (
  `uid` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id` varchar(100) NOT NULL DEFAULT '',
  `pw` varchar(100) NOT NULL DEFAULT '',
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


```
CREATE TABLE `session` (
  `session_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `uid` bigint NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expire_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


```
CREATE TABLE `favorites` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `station_id` int unsigned NOT NULL,
  `uid` bigint unsigned NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

</br></br></br>

# Redis

favorite 관련 redis-stack-server를 사용하기 위한 index 처리

```
FT.CREATE fvrIndex ON JSON PREFIX 1 id: SCHEMA $.station_id as station_id NUMERIC $.uid AS uid NUMERIC
```

</br></br></br>

# DB vs Redis
DB만을 사용했을 때와 redis를 사용했을 때의 select 시간 비교 결과는 다음과 같다.

</br>

### <환경>
- 총 데이터 수 : 100011
- 실행한 table : ```favorites```
- random 값 설정 방식 : [```generate_random_values``` 함수 참고]

</br></br>

### <실험 방식>
0~1000 사이의 랜덤 uid 100개를 추출해서,

각각 해당 uid의 favorite 값 리스트를 가져오는 시간을 가져온다.

구한 시간의 평균값을 낸다.


</br></br>

### <결과>
|대상|실행 시간|
|-------|------------|
| DB    | 22.2847 ms |
| Redis | 1.3277 ms  |

</br>

#### 결론 : redis를 활용하면 16.7배 더 빠르게 실행됐다.

</br></br></br></br>

# 참고한 내용
- https://redis.io/docs/stack/json/
- https://redis.io/docs/stack/search/indexing_json/
- https://redis.io/commands/
- https://velog.io/@grit_munhyeok/Redis-JSON-FastAPI%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%B4-DB%EB%A7%8C%EB%93%A4%EA%B8%B0