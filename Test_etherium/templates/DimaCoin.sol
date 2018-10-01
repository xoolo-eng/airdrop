// pragma solidity ^0.4.24

/**
 * The Super contract does this and that...
 */
contract DimaCoin {
    uint public totalSupply = 20000000000000000000000000;
    string public constant name = "Dima Coim";
    string public constant symbol = "DCN";
    uint8 public constant decimals = 18;
    mapping (address => mapping (address => uint)) allowed;
    mapping (address => uint) balances;
    function DimaCoin() {
        balances[msg.sender] = totalSupply;
    }
    function balanceOf(address owner) public constant returns (uint) {
        return balances[owner];
    }
    function transfer(address to, uint value) public {
        if (balances[msg.sender] >= value) {
            balances[msg.sender] -= value;
            balances[to] += value;
            emit Transfer(msg.sender, to, value);
        }
    }
    function allowance(address owner, address spender) public constant returns (uint) {
        return allowed[owner][spender];
    }
    function transferFrom(address from, address to, uint value) public {
        if (allowed[from][msg.sender] >= value && balances[from] >= value) {
            balances[to] +=value;
            balances[from] -= value;
            allowed[from][msg.sender] -= value;
            emit Transfer(from, to, value);
        }
    }
    function approve(address spender, uint value) public {
        allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
    }
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);    
}