Blockly.Python['dispo_out'] = function(block) {
  var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('dispo'), Blockly.Variables.NAME_TYPE);
  var number_name = block.getFieldValue('var');
  // TODO: Assemble Python into code variable.
  var code = 'save '+variable_name+' '+number_name+'\n';
  return code;
};

Blockly.Python['sen_se'] = function(block) {
  var dropdown_sensores = block.getFieldValue('sensores');
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_se = Blockly.Python.valueToCode(block, 'Se', Blockly.Python.ORDER_ATOMIC);
  var statements_se_sta = Blockly.Python.statementToCode(block, 'Se_sta');
  var code = 'se '+dropdown_sensores+' '+ dropdown_condicao+' '+value_se+'\n'+statements_se_sta+"\n";
  return code;
};

Blockly.Python['save_db'] = function(block) {
  var code = 'save_database;\n';
  return code;
};

Blockly.Python['atuador_troca_estado'] = function(block) {
  var dropdown_dispositivo = block.getFieldValue('dispositivo');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['atuador_boolean'] = function(block) {
  var value_estado = Blockly.Python.valueToCode(block, 'estado', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['if_sensor_string'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dado = Blockly.Python.valueToCode(block, 'dado', Blockly.Python.ORDER_ATOMIC);
  var statements_if = Blockly.Python.statementToCode(block, 'if');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['if_sensor_number'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_valor = Blockly.Python.valueToCode(block, 'valor', Blockly.Python.ORDER_ATOMIC);
  var statements_if = Blockly.Python.statementToCode(block, 'if');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['dado_sensor_numero'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['dado_sensor_string'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['if_sensor_dadosensornumero'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dados = Blockly.Python.valueToCode(block, 'dados', Blockly.Python.ORDER_ATOMIC);
  var statements_if = Blockly.Python.statementToCode(block, 'if');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['if_sensor_boolena'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dado = Blockly.Python.valueToCode(block, 'dado', Blockly.Python.ORDER_ATOMIC);
  var statements_if = Blockly.Python.statementToCode(block, 'if');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};

Blockly.Python['dados_sensor_media'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['dado_sensor_min'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['dado_sensor_max'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['if_sensor_dadosensorstring'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dados = Blockly.Python.valueToCode(block, 'dados', Blockly.Python.ORDER_ATOMIC);
  var statements_if = Blockly.Python.statementToCode(block, 'if');
  // TODO: Assemble Python into code variable.
  var code = '...;\n';
  return code;
};