package main

import (
    "bufio"
    "flag"
    "fmt"
    "os"
    "os/user"
    "path/filepath"
    "strings"
    "text/tabwriter"
)

var charMap = map[rune]int{
    ' ': 0,
    '\t': 0,
    '\n': 0,
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 8,
    'g': 3,
    'h': 5,
    'i': 1,
    'j': 1,
    'k': 2,
    'l': 3,
    'm': 4,
    'n': 5,
    'o': 7,
    'p': 8,
    'q': 1,
    'r': 2,
    's': 3,
    't': 4,
    'u': 6,
    'v': 6,
    'w': 6,
    'x': 5,
    'y': 1,
    'z': 7,
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 8,
    'G': 3,
    'H': 5,
    'I': 1,
    'J': 1,
    'K': 2,
    'L': 3,
    'M': 4,
    'N': 5,
    'O': 7,
    'P': 8,
    'Q': 1,
    'R': 2,
    'S': 3,
    'T': 4,
    'U': 6,
    'V': 6,
    'W': 6,
    'X': 5,
    'Y': 1,
    'Z': 7,
}

const vowels = "aeiou"

func main() {
    mode := flag.String("mode", "sum", "Operation mode: sum, generate, search")
    name := flag.String("name", "", "Name to calculate numerology for")
    prefix := flag.String("prefix", "", "Prefix for generated names")
    desired := flag.Int("desired", 0, "Desired numerology sum for generated names")
    maxLength := flag.Int("max-length", 0, "Maximum length for generated names")
    dictionary := flag.String("dictionary", "", "Path to a dictionary file with one name per line")
    startsWith := flag.String("starts-with", "", "Filter dictionary names starting with this text")
    nameSum := flag.Int("name-sum", 0, "Filter dictionary results by exact name sum")
    recursiveSum := flag.Int("recursive-sum", 0, "Filter dictionary results by exact recursive sum")
    initial := flag.String("initial", "", "Initial to use for full names (default is first letter of OS username)")
    flag.Parse()

    switch strings.ToLower(*mode) {
    case "sum":
        if *name == "" {
            fmt.Fprintln(os.Stderr, "Error: --name is required for mode=sum")
            flag.Usage()
            os.Exit(1)
        }
        printNameSums(*name)
    case "generate":
        if *desired <= 0 || *maxLength <= 0 {
            fmt.Fprintln(os.Stderr, "Error: --desired and --max-length must be greater than zero for mode=generate")
            flag.Usage()
            os.Exit(1)
        }
        printGeneratedNames(*prefix, *maxLength, *desired)
    case "search":
        if *dictionary == "" {
            fmt.Fprintln(os.Stderr, "Error: --dictionary is required for mode=search")
            flag.Usage()
            os.Exit(1)
        }
        printDictionarySearch(*dictionary, *startsWith, *nameSum, *recursiveSum, *initial)
    default:
        fmt.Fprintf(os.Stderr, "Unknown mode: %s\n", *mode)
        flag.Usage()
        os.Exit(1)
    }
}

func isVowel(r rune) bool {
    return strings.ContainsRune(vowels, unicodeToLower(r))
}

func unicodeToLower(r rune) rune {
    if 'A' <= r && r <= 'Z' {
        return r + ('a' - 'A')
    }
    return r
}

func findSum(name string) int {
    total := 0
    for _, r := range name {
        total += charMap[r]
    }
    return total
}

func digitSum(number int) int {
    total := 0
    for number > 0 {
        total += number % 10
        number /= 10
    }
    return total
}

func findRecursiveSum(number int) int {
    for number > 9 {
        number = digitSum(number)
    }
    return number
}

func printNameSums(name string) {
    total := findSum(name)
    recursive := findRecursiveSum(total)
    fmt.Printf("Name: %s\n", name)
    fmt.Printf("Sum: %d\n", total)
    fmt.Printf("Recursive Sum: %d\n", recursive)
}

func printGeneratedNames(prefix string, maxLength, desiredSum int) {
    fmt.Printf("Prefix: %s\n", prefix)
    fmt.Printf("Desired Sum: %d\n", desiredSum)
    fmt.Printf("Max Length: %d\n\n", maxLength)
    names := generateNames(prefix, maxLength, desiredSum)
    if len(names) == 0 {
        fmt.Println("No matching names found.")
        return
    }
    for _, name := range names {
        fmt.Println(name)
    }
}

func generateNames(prefix string, maxLength, desiredSum int) []string {
    if maxLength <= 0 {
        return nil
    }

    prefixSum := findSum(prefix)
    if desiredSum <= prefixSum {
        return nil
    }

    remaining := maxLength - len([]rune(prefix))
    if remaining < 0 {
        return nil
    }

    var results []string
    generateNameTree(prefix, remaining, desiredSum-prefixSum, &results)
    return results
}

func generateNameTree(prefix string, maxLength, desiredSum int, results *[]string) {
    if maxLength <= 0 {
        return
    }

    lastChar := rune(0)
    if len(prefix) > 0 {
        lastChar = rune(prefix[len(prefix)-1])
    }

    for r := 'a'; r <= 'z'; r++ {
        if lastChar == r {
            continue
        }
        if isVowel(r) && isVowel(lastChar) {
            continue
        }

        candidate := prefix + string(r)
        value := charMap[r]
        if value >= desiredSum {
            if value == desiredSum {
                *results = append(*results, candidate)
            }
            continue
        }

        generateNameTree(candidate, maxLength-1, desiredSum-value, results)
    }
}

func printDictionarySearch(dictionaryPath, startsWith string, nameSum, recursiveSum int, initial string) {
    path := filepath.Clean(dictionaryPath)
    names, err := loadDictionary(path)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error loading dictionary: %v\n", err)
        os.Exit(1)
    }

    if initial == "" {
        initial = defaultInitial()
    }

    writer := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
    fmt.Fprintln(writer, "Name\tInitial\tLast Name\tSum\tRecursive Sum\tFull Name")

    for _, name := range names {
        normalized := strings.TrimSpace(name)
        if normalized == "" {
            continue
        }
        if startsWith != "" && !strings.HasPrefix(strings.ToLower(normalized), strings.ToLower(startsWith)) {
            continue
        }

        sum := findSum(normalized)
        if nameSum != 0 && sum != nameSum {
            continue
        }

        term := findRecursiveSum(sum)
        if recursiveSum != 0 && term != recursiveSum {
            continue
        }

        lastName := computeLastName(normalized)
        fullName := computeFullName(normalized, initial)
        fmt.Fprintf(writer, "%s\t%s\t%s\t%d\t%d\t%s\n", normalized, strings.ToUpper(initial), lastName, sum, term, fullName)
    }

    writer.Flush()
}

func loadDictionary(path string) ([]string, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var names []string
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }
        names = append(names, line)
    }
    return names, scanner.Err()
}

func computeLastName(name string) string {
    fields := strings.Fields(name)
    if len(fields) == 0 {
        return ""
    }
    return fields[len(fields)-1]
}

func computeFullName(name, initial string) string {
    if initial == "" {
        return name
    }
    return fmt.Sprintf("%s %s", name, strings.ToUpper(initial))
}

func defaultInitial() string {
    current, err := user.Current()
    if err != nil || current.Username == "" {
        return ""
    }
    if len(current.Username) == 0 {
        return ""
    }
    return strings.ToUpper(current.Username[:1])
}
