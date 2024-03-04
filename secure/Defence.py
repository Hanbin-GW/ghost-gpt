from scapy.all import sniff, IP
from collections import defaultdict

# IP 주소별 트래픽 양을 추적하는 딕셔너리
traffic_counter = defaultdict(int)

# 차단된 IP 주소를 저장하는 집합
blocked_ips = set()

# 트래픽 임계값 (예: 500GB를 바이트로 환산)
TRAFFIC_LIMIT = 500 * 1024**3  # 500GB

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        # 패킷의 크기를 트래픽 양으로 추정
        packet_size = len(packet)
        
        # 이미 차단된 IP 주소의 트래픽은 무시
        if ip_src in blocked_ips:
            return
        
        # 트래픽 양 업데이트
        traffic_counter[ip_src] += packet_size
        
        # 트래픽 임계값 초과 검사
        if traffic_counter[ip_src] > TRAFFIC_LIMIT:
            # IP 차단
            blocked_ips.add(ip_src)
            print(f"IP {ip_src} has been blocked due to excessive traffic.")

# 패킷 캡처 시작
sniff(prn=packet_callback, filter="ip", store=False)
