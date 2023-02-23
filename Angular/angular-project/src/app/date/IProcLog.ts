export interface ProcLog {
    id: number
    command: string
    extid_action: string
    is_complite: boolean
    stdout: string
    date_start: Date
    code_return: number
}