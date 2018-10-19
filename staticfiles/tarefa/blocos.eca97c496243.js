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

Blockly.JavaScript['save_db'] = function(block) {
  var code = 'save_database;\n';
  return code;
};

Blockly.JavaScript['atuador_troca_estado'] = function(block) {
  var dropdown_dispositivo = block.getFieldValue('dispositivo');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['atuador_boolean'] = function(block) {
  var value_estado = Blockly.JavaScript.valueToCode(block, 'estado', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['if_sensor_string'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dado = Blockly.JavaScript.valueToCode(block, 'dado', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if = Blockly.JavaScript.statementToCode(block, 'if');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['if_sensor_number'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_valor = Blockly.JavaScript.valueToCode(block, 'valor', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if = Blockly.JavaScript.statementToCode(block, 'if');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['dado_sensor_numero'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['dado_sensor_string'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['if_sensor_dadosensornumero'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dados = Blockly.JavaScript.valueToCode(block, 'dados', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if = Blockly.JavaScript.statementToCode(block, 'if');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['if_sensor_boolena'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dado = Blockly.JavaScript.valueToCode(block, 'dado', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if = Blockly.JavaScript.statementToCode(block, 'if');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['dados_sensor_media'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['dado_sensor_min'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['dado_sensor_max'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['if_sensor_dadosensorstring'] = function(block) {
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_dados = Blockly.JavaScript.valueToCode(block, 'dados', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if = Blockly.JavaScript.statementToCode(block, 'if');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};