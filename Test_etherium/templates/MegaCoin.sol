// pragma solidity ^{{version}};
// pragma solidity ^0.4.24;
contract ERC20 {
    uint public totalSupply = {{ count_token }};
    function balanceOf(address owner) public constant returns (uint);
    function transfer(address to, uint value) public;
    function allowance(address owner, address spender) public constant returns (uint);

    function transferFrom(address from, address to, uint value) public;
    function approve(address spender, uint value) public;

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}

contract {{name.class}} is ERC20 {
    uint public requestedSupply;
    string public constant name = "{{name.name}}";
    string public constant symbol = "{{name.symbol}}";
    uint8 public constant decimals = 18;

    mapping (address => mapping (address => uint)) allowed;
    mapping (address => uint) balances;

    constructor() public {
        balances[msg.sender] = {{count_token}};
    }

    function transferFrom(address _from, address _to, uint _value) public {
        balances[_to] += _value;
        balances[_from] -= _value;
        allowed[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
    }

    function approve(address _spender, uint _value) public {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
    }

    function allowance(address _owner, address _spender) public constant returns (uint remaining) {
        return allowed[_owner][_spender];
    }

    function transfer(address _to, uint _value) public {
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
    }

    function balanceOf(address _owner) public constant returns (uint balance) {
        return balances[_owner];
    }
}