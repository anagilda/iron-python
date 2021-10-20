const { seal, defaults } = require("@hapi/iron");

/**
 * Parse arguments from the command line input.
 *
 * @param {string[]} argumentNames the names of the arguments to parse from command line input.
 * @return {{}} a record of the selected parsed arguments.
 */
function getCommandArguments(argumentNames) {
    const parsedArguments = process.argv.reduce((accumulator, argument) => {
        const [name, value] = argument.split("=");
        if (argumentNames.includes(name)) accumulator[name] = value;
        return accumulator;
    }, {});

    return parsedArguments;
}

/**
 * Get an encrypted cookie containing the token data.
 * The token is sealed using the provided encryption password.
 *
 * @return {Promise<string>} encrypted cookie.
 */
async function getEncryptedCookie() {
    try {
        const { password, token } = getCommandArguments(["password", "token"]);
        return await seal({ token }, password, defaults);
    } catch (error) {
        console.error(error);
    }
}

function main() {
    getEncryptedCookie().then((result) => console.log(result));
}

main();
