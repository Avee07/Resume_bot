import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from parser_utils import parse_file, to_json
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a resume (PDF or DOCX) as a document and I'll parse it to JSON.")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a document (PDF or DOCX). I'll reply with a JSON file containing parsed fields.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    fname = doc.file_name
    logger.info(f"Received file: {fname} from {update.effective_user.id}")

    # download the file to a temp file
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(fname)[1], delete=False) as tf:
        file_path = tf.name
        await doc.get_file().download_to_drive(file_path)

    try:
        with open(file_path, 'rb') as f:
            parsed = parse_file(fname, content_type=doc.mime_type, file_obj=f)

        json_str = to_json(parsed)

        # send back as a file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w', encoding='utf-8') as out:
            out.write(json_str)
            out_path = out.name

        await update.message.reply_text("Parsed resume — sending JSON file.")
        await update.message.reply_document(document=InputFile(out_path), filename=f"{os.path.splitext(fname)[0]}.json")
    except Exception as e:
        logger.exception('Error parsing file')
        await update.message.reply_text(f"Sorry, couldn't parse the file: {e}")
    finally:
        try:
            os.unlink(file_path)
        except Exception:
            pass


def main():
    token = os.environ.get('TG_BOT_TOKEN')
    if not token:
        raise RuntimeError('Set TG_BOT_TOKEN environment variable')

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    logger.info('Starting bot...')
    app.run_polling()


if __name__ == '__main__':
    main()
