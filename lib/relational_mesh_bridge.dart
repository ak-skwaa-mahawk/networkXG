// lib/relational_mesh_bridge.dart
import 'package:flutter/services.dart';

class RelationalMeshBridge {
  static final RelationalMeshBridge _instance = RelationalMeshBridge._();
  factory RelationalMeshBridge() => _instance;
  RelationalMeshBridge._();

  final _channel = const MethodChannel('networkxg/relational_mesh');

  Future<void> initialize() async {
    await _channel.invokeMethod('startRelationalMesh'); // launches Python backend
  }

  Future<void> propagateMetric(SovereignMetric metric) async {
    await _channel.invokeMethod('propagateSoliton', {
      'pose': metric.pose,
      'stability': metric.stabilityScore,
      'resonance': metric.resonanceDelta,
      'pulseHz': 79.79,
    });
  }

  Future<void> triggerConstellationHandshake() async {
    await _channel.invokeMethod('constellationHandshake');
  }
}