# アクティブウィンドウTTSアプリ仕様書ナリ

## 概要ナリ
本アプリケーションは、Windows環境上でアクティブなウィンドウから日本語のテキストを取得し、ローカルのTTSサーバーAPIを呼び出して音声を再生するツールであるナリ。ユーザーはこれにより、画面上の日本語テキストを手軽に音声化できるナリ。

## 機能要件ナリ
1. **アクティブウィンドウの検出ナリ：**  
   Windows APIを用いて、現在アクティブなウィンドウのハンドルとウィンドウ領域を取得するナリ。

2. **スクリーンショット取得ナリ：**  
   - アクティブウィンドウの領域のスクリーンショットを取得するナリ。
   - PIL (Python Imaging Library) を使用して画像データを処理するナリ。

3. **OCRによるテキスト抽出ナリ：**  
   - Tesseract-OCRを使用して日本語テキストを抽出するナリ。
   - OCRの設定は日本語に最適化（`-l jpn`）するナリ。
   - 必要に応じて画像の前処理（二値化、ノイズ除去など）を実施するナリ。

4. **TTS API呼び出しナリ：**  
   OCRで抽出した日本語テキストをローカルのTTSサーバーAPIに送信し、音声データを生成するナリ。  
   - HTTP POST リクエストを使用するナリ。  
   - 例: `{ "text": "OCRで抽出したテキスト" }` という形式でリクエストするナリ。

   # AivisSpeech Engine v1.0.0

AivisSpeech の音声合成エンジンです。


## POST /audio_query


音声合成用のクエリを作成する


音声合成用のクエリの初期値を得ます。ここで得られたクエリはそのまま音声合成に利用できます。各値の意味は`Schemas`を参照してください。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | ? |  |
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/AudioQuery"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /audio_query_from_preset


音声合成用のクエリをプリセットを用いて作成する


音声合成用のクエリの初期値を得ます。ここで得られたクエリはそのまま音声合成に利用できます。各値の意味は`Schemas`を参照してください。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | ? |  |
| preset_id | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/AudioQuery"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /accent_phrases


テキストからアクセント句を得る


テキストからアクセント句を得ます。
is_kanaが`true`のとき、テキストは次の AquesTalk 風記法で解釈されます。デフォルトは`false`です。
* 全てのカナはカタカナで記述される
* アクセント句は`/`または`、`で区切る。`、`で区切った場合に限り無音区間が挿入される。
* カナの手前に`_`を入れるとそのカナは無声化される
* アクセント位置を`'`で指定する。全てのアクセント句にはアクセント位置を1つ指定する必要がある。
* アクセント句末に`？`(全角)を入れることにより疑問文の発音ができる。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | ? |  |
| speaker | integer | ? |  |
| is_kana | boolean |  |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/AccentPhrase"
  },
  "title": "Response Accent Phrases Accent Phrases Post"
}
```

#### 400

読み仮名のパースに失敗

```json
{
  "$ref": "#/components/schemas/ParseKanaBadRequest"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /mora_data


アクセント句から音高・音素長を得る


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/AccentPhrase"
  },
  "title": "Response Mora Data Mora Data Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /mora_length


アクセント句から音素長を得る


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/AccentPhrase"
  },
  "title": "Response Mora Length Mora Length Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /mora_pitch


アクセント句から音高を得る


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/AccentPhrase"
  },
  "title": "Response Mora Pitch Mora Pitch Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /synthesis


音声合成する


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| enable_interrogative_upspeak | boolean |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /cancellable_synthesis


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /multi_synthesis


複数まとめて音声合成する


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /sing_frame_audio_query


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/FrameAudioQuery"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /sing_frame_volume


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "type": "number"
  },
  "title": "Response Sing Frame Volume Sing Frame Volume Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /frame_synthesis


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /connect_waves


base64エンコードされた複数のwavデータを一つに結合する


base64エンコードされたwavデータを一纏めにし、wavファイルで返します。


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /validate_kana


テキストが AquesTalk 風記法に従っているか判定する


テキストが AquesTalk 風記法に従っているかどうかを判定します。
従っていない場合はエラーが返ります。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| text | string | ? | 判定する対象の文字列 |


### Responses

#### 200

Successful Response

```json
{
  "type": "boolean",
  "title": "Response Validate Kana Validate Kana Post"
}
```

#### 400

テキストが不正です

```json
{
  "$ref": "#/components/schemas/ParseKanaBadRequest"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /initialize_speaker


Initialize Speaker


指定されたスタイルを初期化します。
実行しなくても他のAPIは使用できますが、初回実行時に時間がかかることがあります。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| skip_reinit | boolean |  | 既に初期化済みのスタイルの再初期化をスキップするかどうか |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /is_initialized_speaker


Is Initialized Speaker


指定されたスタイルが初期化されているかどうかを返します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker | integer | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "type": "boolean",
  "title": "Response Is Initialized Speaker Is Initialized Speaker Get"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /supported_devices


Supported Devices


対応デバイスの一覧を取得します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/SupportedDevicesInfo"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /morphable_targets


指定したスタイルに対してエンジン内のキャラクターがモーフィングが可能か判定する


指定されたベーススタイルに対してエンジン内の各キャラクターがモーフィング機能を利用可能か返します。
モーフィングの許可/禁止は `/speakers `の `speaker.supported_features.synthesis_morphing` に記載されています。
プロパティが存在しない場合は、モーフィングが許可されているとみなします。
返り値のスタイル ID は string 型なので注意。
AivisSpeech Engine では話者ごとに発声タイミングが異なる関係で実装不可能なため (動作こそするが聴くに耐えない) 、
全ての話者でモーフィングが禁止されています。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "additionalProperties": {
      "$ref": "#/components/schemas/MorphableTargetInfo"
    }
  },
  "title": "Response Morphable Targets Morphable Targets Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /synthesis_morphing


2種類のスタイルでモーフィングした音声を合成する


指定された 2 種類のスタイルで音声を合成、指定した割合でモーフィングした音声を得ます。
モーフィングの割合は `morph_rate` で指定でき、0.0 でベースのスタイル、1.0 でターゲットのスタイルに近づきます。
AivisSpeech Engine では話者ごとに発声タイミングが異なる関係で実装不可能なため (動作こそするが聴くに耐えない) 、
常に 400 Bad Request を返します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| base_speaker | integer | ? |  |
| target_speaker | integer | ? |  |
| morph_rate | number | ? |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Request Body



### Responses

#### 200

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /presets


Get Presets


エンジンが保持しているプリセットの設定を返します


### Responses

#### 200

プリセットのリスト

```json
{
  "items": {
    "$ref": "#/components/schemas/Preset"
  },
  "type": "array",
  "title": "Response Get Presets Presets Get"
}
```



## POST /add_preset


Add Preset


新しいプリセットを追加します


### Request Body



### Responses

#### 200

追加したプリセットのプリセットID

```json
{
  "type": "integer",
  "title": "Response Add Preset Add Preset Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /update_preset


Update Preset


既存のプリセットを更新します


### Request Body



### Responses

#### 200

更新したプリセットのプリセットID

```json
{
  "type": "integer",
  "title": "Response Update Preset Update Preset Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /delete_preset


Delete Preset


既存のプリセットを削除します


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | integer | ? | 削除するプリセットのプリセットID |


### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /speakers


Speakers


喋れるキャラクターの情報の一覧を返します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/Speaker"
  },
  "title": "Response Speakers Speakers Get"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /speaker_info


Speaker Info


UUID で指定された喋れるキャラクターの情報を返します。
画像や音声はresource_formatで指定した形式で返されます。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker_uuid | string | ? |  |
| resource_format | string |  |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/SpeakerInfo"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /singers


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "type": "array",
  "items": {
    "$ref": "#/components/schemas/Speaker"
  },
  "title": "Response Singers Singers Get"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /singer_info


AivisSpeech Engine ではサポートされていない API です (常に 501 Not Implemented を返します)


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| speaker_uuid | string | ? |  |
| resource_format | string |  |  |
| core_version | string |  | AivisSpeech Engine ではサポートされていないパラメータです (常に無視されます) 。 |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/SpeakerInfo"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /aivm_models


Get Installed Aivm Infos


インストールした音声合成モデルの情報を返します。


### Responses

#### 200

インストールした音声合成モデルの情報

```json
{
  "additionalProperties": {
    "$ref": "#/components/schemas/AivmInfo"
  },
  "type": "object",
  "title": "Response Get Installed Aivm Infos Aivm Models Get"
}
```



## POST /aivm_models/install


Install Aivm


音声合成モデルをインストールします。
ファイルからインストールする場合は `file` を指定してください。
URL からインストールする場合は `url` を指定してください。


### Request Body



### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /aivm_models/{aivm_uuid}


Get Aivm Info


指定された音声合成モデルの情報を取得します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| aivm_uuid | string | ? | 音声合成モデルの UUID |


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/AivmInfo"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## DELETE /aivm_models/{aivm_uuid}/uninstall


Uninstall Aivm


指定された音声合成モデルをアンインストールします。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| aivm_uuid | string | ? | 音声合成モデルの UUID |


### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /user_dict


Get User Dict Words


ユーザー辞書に登録されている単語の一覧を返します。
単語の表層形(surface)は正規化済みの物を返します。


### Responses

#### 200

単語のUUIDとその詳細

```json
{
  "additionalProperties": {
    "$ref": "#/components/schemas/UserDictWord"
  },
  "type": "object",
  "title": "Response Get User Dict Words User Dict Get"
}
```



## POST /user_dict_word


Add User Dict Word


ユーザー辞書に言葉を追加します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| surface | string | ? | 言葉の表層形 |
| pronunciation | string | ? | 言葉の発音（カタカナ） |
| accent_type | integer | ? | アクセント型（音が下がる場所を指す） |
| word_type |  |  | PROPER_NOUN（固有名詞）、COMMON_NOUN（普通名詞）、VERB（動詞）、ADJECTIVE（形容詞）、SUFFIX（語尾）のいずれか |
| priority | integer |  | 単語の優先度（0から10までの整数）。数字が大きいほど優先度が高くなる。1から9までの値を指定することを推奨 |


### Responses

#### 200

Successful Response

```json
{
  "type": "string",
  "title": "Response Add User Dict Word User Dict Word Post"
}
```

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## PUT /user_dict_word/{word_uuid}


Rewrite User Dict Word


ユーザー辞書に登録されている言葉を更新します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| word_uuid | string | ? | 更新する言葉のUUID |
| surface | string | ? | 言葉の表層形 |
| pronunciation | string | ? | 言葉の発音（カタカナ） |
| accent_type | integer | ? | アクセント型（音が下がる場所を指す） |
| word_type |  |  | PROPER_NOUN（固有名詞）、COMMON_NOUN（普通名詞）、VERB（動詞）、ADJECTIVE（形容詞）、SUFFIX（語尾）のいずれか |
| priority | integer |  | 単語の優先度（0から10までの整数）。数字が大きいほど優先度が高くなる。1から9までの値を指定することを推奨。 |


### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## DELETE /user_dict_word/{word_uuid}


Delete User Dict Word


ユーザー辞書に登録されている言葉を削除します。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| word_uuid | string | ? | 削除する言葉のUUID |


### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## POST /import_user_dict


Import User Dict Words


他のユーザー辞書をインポートします。


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| override | boolean | ? | 重複したエントリがあった場合、上書きするかどうか |


### Request Body



### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /version


Version


エンジンのバージョンを取得します。


### Responses

#### 200

Successful Response

```json
{
  "type": "string",
  "title": "Response Version Version Get"
}
```



## GET /core_versions


Core Versions


利用可能なコアのバージョン一覧を取得します。


### Responses

#### 200

Successful Response

```json
{
  "items": {
    "type": "string"
  },
  "type": "array",
  "title": "Response Core Versions Core Versions Get"
}
```



## GET /engine_manifest


Engine Manifest


エンジンマニフェストを取得します。


### Responses

#### 200

Successful Response

```json
{
  "$ref": "#/components/schemas/EngineManifest"
}
```



## GET /setting


Setting Get


設定ページを返します。


### Responses

#### 200

Successful Response



## POST /setting


Setting Post


設定を更新します。


### Request Body



### Responses

#### 204

Successful Response

#### 422

Validation Error

```json
{
  "$ref": "#/components/schemas/HTTPValidationError"
}
```



## GET /


Get Portal Page


ポータルページを返します。


### Responses

#### 200

Successful Response

話者IDについて
[
{
"name": "Anneli",
"speaker_uuid": "e756b8e4-b606-4e15-99b1-3f9c6a1b2317",
"styles": [
{
"name": "ノーマル",
"id": 888753760,
"type": "talk"
},
{
"name": "通常",
"id": 888753761,
"type": "talk"
},
{
"name": "テンション高め",
"id": 888753762,
"type": "talk"
},
{
"name": "落ち着き",
"id": 888753763,
"type": "talk"
},
{
"name": "上機嫌",
"id": 888753764,
"type": "talk"
},
{
"name": "怒り・悲しみ",
"id": 888753765,
"type": "talk"
}
],
"version": "1.0.0",
"supported_features": {
"permitted_synthesis_morphing": "NOTHING"
}
},
{
"name": "korosuke",
"speaker_uuid": "40e5743b-a55b-4703-9cd7-221e3e5696a5",
"styles": [
{
"name": "ノーマル",
"id": 488039072,
"type": "talk"
}
],
"version": "1.0.0",
"supported_features": {
"permitted_synthesis_morphing": "NOTHING"
}
},
{
"name": "sakuragi",
"speaker_uuid": "e4dbb14f-6b40-4a00-a674-c6043b1412a5",
"styles": [
{
"name": "ノーマル",
"id": 269244800,
"type": "talk"
}
],
"version": "1.0.0",
"supported_features": {
"permitted_synthesis_morphing": "NOTHING"
}
}


5. **音声再生ナリ：**  
   TTSサーバーから返された音声データを、ローカル環境で再生するナリ。

6. **エラーハンドリングナリ：**  
   - アクティブウィンドウの取得に失敗した場合  
   - スクリーンショット取得に失敗した場合  
   - OCR処理に失敗した場合  
   - TTSサーバーからの応答が得られなかった場合  
   など、各種エラー発生時に適切なエラーメッセージを表示し、必要に応じてリトライ処理を実施するナリ。

## 非機能要件ナリ
- **OS:** Windows環境専用ナリ。
- **使用言語:** Python（推奨）ナリ。
- **ライブラリインストール:** Pythonライブラリのインストールは `uv install <ライブラリ名>` コマンドを使用するナリ。
- **コマンド連結:** Windows環境ではコマンド連結に `;` を使用するナリ。
- **セキュリティ:**  
   - 機密情報は `.env` ファイルで管理し、GitHub へは `.env.sample` として機密情報を削除した状態で push するナリ。
   - API通信はローカルネットワーク内で行うため、外部からの不正アクセスに注意するナリ。
- **OCR要件:**
  - Tesseract-OCR v5.0以上を使用するナリ。
  - 日本語言語パックのインストールが必要ナリ。
- **画像処理要件:**
  - スクリーンショットの解像度は元のウィンドウと同じにするナリ。
  - OCRの精度向上のため、必要に応じて画像の前処理を行うナリ。

## システム構成ナリ
- **スクリーンショットモジュールナリ：**  
  `win32gui`と`PIL`を使用してアクティブウィンドウのスクリーンショットを取得するナリ。

- **OCRモジュールナリ：**  
  Tesseract-OCRと`pytesseract`を使用して日本語テキストを抽出するナリ。

- **通信モジュールナリ：**  
  ローカルのTTSサーバーAPIとのHTTP通信を担当するナリ。

- **再生モジュールナリ：**  
  取得した音声データをオーディオ出力デバイスへ送信して再生するナリ。

## 必要なライブラリナリ
以下のライブラリを `uv install` でインストールする必要があるナリ：
- `pywin32` (Windowsシステム操作用)
- `Pillow` (画像処理用)
- `pytesseract` (OCR用)
- `requests` (API通信用)
- `python-dotenv` (環境変数管理用)

## ワークフローナリ
1. **アクティブウィンドウの検出ナリ：**  
   Windows APIを利用して、現在のアクティブなウィンドウのハンドルと領域を取得するナリ。

2. **スクリーンショット取得ナリ：**  
   - アクティブウィンドウの領域を特定するナリ。
   - PILを使用してスクリーンショットを取得するナリ。
   - 必要に応じて画像の前処理を行うナリ。

3. **OCRによるテキスト抽出ナリ：**  
   - Tesseract-OCRで日本語テキストを抽出するナリ。
   - 抽出されたテキストの後処理（不要な改行の削除など）を行うナリ。

4. **TTS API リクエストナリ：**  
   OCRで抽出したテキストをHTTP POSTリクエストにてローカルTTSサーバーに送信するナリ。  
   ※ コマンドラインなどでは連結に `;` を用いるナリ。

5. **音声再生ナリ：**  
   TTSサーバーから返された音声データを受け取り、再生するナリ。

## 開発手順ナリ
1. **環境セットアップナリ：**  
   - Pythonをインストールするナリ。  
   - 必要なPythonライブラリは `uv install` を使用してインストールするナリ。  
   - 機密情報は `.env` ファイルで管理し、GitHub では `.env.sample` としてpushするナリ。

2. **機能実装ナリ：**  
   - アクティブウィンドウ検出機能の実装ナリ。  
   - スクリーンショット取得機能の実装ナリ。  
   - OCRによるテキスト抽出機能の実装ナリ。  
   - TTS API 通信機能の実装ナリ。  
   - 音声再生機能の実装ナリ。

3. **テスト及びデバッグナリ：**  
   各機能に対して、単体テスト及び統合テストを実施し、エラー時のハンドリングの確認を行うナリ。

4. **デプロイナリ：**  
   - コードのGitHubへのpushの際は、機密情報を削除した `.env.sample` を使用するナリ。  
   - Windows環境特有のコマンド連結（`;` 使用）に注意するナリ。

## エラーハンドリングナリ
- アクティブウィンドウが取得できない場合は、ユーザーに対して適切なエラーメッセージを表示するナリ。
- スクリーンショット取得に失敗した場合は、再試行するナリ。
- OCR処理に失敗した場合は、画像の前処理を変更して再試行するナリ。
- OCRの結果が空の場合は、ユーザーに通知するナリ。
- TTSサーバーからの応答が得られなかった場合は、タイムアウトやリトライ処理を実装するナリ。

## セキュリティについてナリ
- `.env` ファイルを直接GitHubにpushしないようにし、機密情報は `.env.sample` にて管理するナリ。
- API通信は必要最低限のセキュリティ対策（例：認証やhttps）を検討するナリ。（ローカル内通信のため基本的には低リスクナリ）

---

以上、Windows上でアクティブウィンドウの日本語テキストを抽出し、ローカルTTSサーバーAPIを通して音声に変換・再生するアプリの仕様書ナリ！ 