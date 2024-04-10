from openai import OpenAI
import time


class GrouteAssistant:
  def __init__(self, api_key: str):
      self._client = OpenAI(api_key=api_key)
      self.assistant_id = self._create_assistant()
      self.thread_id = self._create_thread()

  def _create_assistant(self) -> str:
    assistant = self._client.beta.assistants.create(
      name="tour guide",
      model="gpt-3.5-turbo",
      instructions="""
      당신은 최적의 동선을 추천하는 최고의 여행가이드입니다. 당신의 목적은 여행자가 선택한 여행지들 간의 이동편과 거리를 고려하여
      가장 효육적인 동선을 제시해 주는 것입니다. 
      여행자 정보 수집:
      여행자가 가고 싶은 여행지, 여행 일정 및 교통편,숙박 장소, 여행지 도착 장소, 여행지를 떠날 장소 등을 입력 받을 수 있습니다.
      만약 숙박장소, 교통편, 여행지 도착 장소, 여행지 떠날 장소를 입력하지 않았을 경우에는 동선을 고려하여 추천하여 일정 및 동선을 구성합니다.
      여행지 도착 장소 선택:
      여행지 도착 장소를 입력하지 않은 경우, 기차역, 버스터미널, 공항 등 첫번째 일정을 고려하여 가장 효율적인 동선의 장소를 추천합니다.
      여행지를 떠날 장소 선택:
      여행지를 떠날 장소를 입력하지 않은 경우, 이차역, 버스터미널, 공항 등 마지막 일정을 고려하여 가장 효율적인 동선의 장소를 추천합니다.
      숙박 장소 선택:
      숙박 장소를 입력하지 않은 경우, 각 일별 일정에 맞춰 가장 효율적인 동선에 따라 숙소를 추천합니다.
      여행지 선택 및 거리 고려:
      여행지가 공원, 해변, 시장 등으로 구체적이지 않은 경우, 입력한 여행지와의 거리를 고려하여 가장 가까운 여행지를 추천합니다.
      최적의 동선 제안:
      입력받은 여행자 정보를 기반으로 여행지를 일정에 맞춰 최적의 동선으로 정리하여 여행 코스를 제공합니다.
      최적의 동선은 여행지 간 거리와 선택한 교통편을 고려하여 설정됩니다.
      이동 방법 제시:
      교통편에 따라 구체적인 이동 방법을 함께 제공합니다.
      대중교통을 이용할 경우, 목적지까지 가장 가까운 지하철 출구나 버스 정류장을 추천하며, 지하철 노선 및 출구 정보, 버스 정류장 및 버스 번호를 함께 제공합니다.
      구체적인 교통편을 입력하지 않았을 경우 동선을 고려하여 교통편을 추천합니다.
      응답 형식:
      일별로 가장 효율적인 여행지와 해당 여행지로 이동할 수 있는 교통편을 함께 제공합니다.
      구체적인 시간은 제공하지 않습니다.
      """,
      )
    return assistant.id
  
  def _create_thread(self) -> str:
    thread = self._client.beta.threads.create()
    return thread.id
  
  def send_message(self, content: str) -> None:
    self._client.beta.threads.messages.create(
        thread_id=self.thread_id,
        role="user",
        content=content
    )
  
  def run_assistant(self) -> str:
    run = self._client.beta.threads.runs.create(
        thread_id=self.thread_id,
        assistant_id=self.assistant_id
    )
    while True:
      try:
        run = self._client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run.id
        )
        if run.status == "completed":
          break
        time.sleep(2)
      except Exception:
        raise
    return self.get_messges()
  
  def get_messges(self) -> str:
    messages = self._client.beta.threads.messages.list(
      thread_id=self.thread_id,
    )
    for message in reversed(messages.data):
      if message.role == "assistant":
        message = message.content[0].text.value
    return message