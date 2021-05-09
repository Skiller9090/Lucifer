function Person(firstName, lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
}

const family = {};
family.mother = new Person("Jane", "Smith");
family.father = new Person("John", "Smith");
family.daughter = new Person("Emily", "Smith");

const me = new Person("John", "Smith");

const people = [["John", "Smith"], ["Jane", "Doe"], ["Emily", "Jones"]];

const john = new Person("John", "Smith");
const jane = new Person("Jane", "Doe");
const emily = new Person("Emily", "Jones");


console.table(["apples", "oranges", "bananas"]);
console.table(me);
console.table(people);
console.table(family);
console.table([john, jane, emily], ["firstName"]);


if (lucifer.luciferManager === undefined) {
    console.warn("LuciferManager is not active")
} else {
    console.log("LuciferManager is running version: " + lucifer.luciferManager.version)
}
