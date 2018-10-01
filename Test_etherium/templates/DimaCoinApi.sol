contract ERC20 {
  uint public totalSupply;
  function balanceOf(address who) constant returns (uint);
  function transfer(address to, uint value);
  function allowance(address owner, address spender) constant returns (uint);
  function transferFrom(address from, address to, uint value);
  function approve(address spender, uint value);
  event Transfer(address indexed from, address indexed to, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}

contract DimaCoinApi is ERC20 {
    uint public _totalSupply = 20000000000000000000000000;
    string public constant name = "Dima Coin Api";
    string public constant symbol = "DCA";
    uint8 public constant decimals = 18;
    mapping (address => mapping (address => uint)) allowed;
    mapping (address => uint) balances;
    function DimaCoinApi() {
        balances[msg.sender] = _totalSupply;
    }
    function balanceOf(address _owner) public constant returns (uint) {
        return balances[_owner];
    }
    function transfer(address _to, uint _value) public {
        if (balances[msg.sender] >= _value) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
        }
    }
    function allowance(address _owner, address _spender) public constant returns (uint) {
        return allowed[_owner][_spender];
    }
    function transferFrom(address _from, address _to, uint _value) public {
        if (allowed[_from][msg.sender] >= _value && balances[_from] >= _value) {
            balances[_to] +=_value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            emit Transfer(_from, _to, _value);
        }
    }
    function approve(address _spender, uint _value) public {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
    }
}